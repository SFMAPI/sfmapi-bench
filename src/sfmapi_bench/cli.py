from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .api_surface import ApiSurfaceSpec, check_api_surface
from .presets import PRESETS


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sfmapi-bench")
    subcommands = parser.add_subparsers(dest="command", required=True)

    list_presets = subcommands.add_parser("list-presets", help="List built-in presets.")
    list_presets.set_defaults(func=_list_presets)

    api = subcommands.add_parser(
        "api-surface",
        help="Check a live sfmapi backend action catalog.",
    )
    api.add_argument("--base-url", default="http://127.0.0.1:8000")
    api.add_argument("--timeout", type=float, default=30.0)
    api.add_argument("--preset", choices=sorted(PRESETS), default="generic")
    api.add_argument("--spec", type=Path, help="JSON API-surface spec to merge with the preset.")
    api.add_argument("--expect-action", action="append", default=[])
    api.add_argument("--forbid-action", action="append", default=[])
    api.add_argument("--forbid-prefix", action="append", default=[])
    api.add_argument("--require-input-schemas", action="store_true")
    api.add_argument("--require-output-schemas", action="store_true")
    api.add_argument("--quiet", action="store_true", help="Only print JSON on failure.")
    api.set_defaults(func=_api_surface)
    return parser


def _list_presets(args: argparse.Namespace) -> int:
    for name in sorted(PRESETS):
        print(name)
    return 0


def _api_surface(args: argparse.Namespace) -> int:
    spec = PRESETS[args.preset]
    if args.spec:
        spec = _merge_specs(spec, ApiSurfaceSpec.from_file(args.spec))
    spec = spec.merged(
        expected_actions=args.expect_action,
        forbidden_actions=args.forbid_action,
        forbidden_prefixes=args.forbid_prefix,
        require_input_schemas=True if args.require_input_schemas else None,
        require_output_schemas=True if args.require_output_schemas else None,
    )
    result = check_api_surface(args.base_url, spec, timeout=args.timeout)
    if not args.quiet or not result.ok:
        print(json.dumps(result.to_json(), indent=2, sort_keys=True))
    return 0 if result.ok else 1


def _merge_specs(base: ApiSurfaceSpec, override: ApiSurfaceSpec) -> ApiSurfaceSpec:
    return ApiSurfaceSpec(
        name=override.name if override.name != "custom" else base.name,
        expected_actions=base.expected_actions | override.expected_actions,
        forbidden_actions=base.forbidden_actions | override.forbidden_actions,
        forbidden_prefixes=(*base.forbidden_prefixes, *override.forbidden_prefixes),
        require_input_schemas=base.require_input_schemas or override.require_input_schemas,
        require_output_schemas=base.require_output_schemas or override.require_output_schemas,
    )


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
