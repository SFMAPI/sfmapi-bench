from __future__ import annotations

from .api_surface import ApiSurfaceSpec

HLOC_EXPECTED_ACTIONS = frozenset(
    {
        "hloc.convertModel",
        "hloc.extractFeatures",
        "hloc.listConfigs",
        "hloc.localizeSfm",
        "hloc.matchDense",
        "hloc.matchFeatures",
        "hloc.pairsCovisibility",
        "hloc.pairsExhaustive",
        "hloc.pairsPoses",
        "hloc.pairsRetrieval",
        "hloc.reconstruct",
        "hloc.runModule",
        "hloc.runPipeline",
        "hloc.triangulate",
    }
)

HLOC_FORBIDDEN_ACTIONS = frozenset(
    {
        "hloc.localizeInLoc",
        "hloc.colmapFromNvm",
        "hloc.pipelineAachen",
        "hloc.pipelineAachenV11",
        "hloc.pipelineAachenV11LoFTR",
        "hloc.pipelineRobotCar",
        "hloc.pipelineRobotCarColmapFromNvm",
        "hloc.pipelineCMU",
        "hloc.pipelineCambridge",
        "hloc.pipelineSevenScenes",
        "hloc.pipelineSevenScenesCorrectDepth",
        "hloc.pipelineFourSeasonsPrepareReference",
        "hloc.pipelineFourSeasonsLocalize",
    }
)

PRESETS: dict[str, ApiSurfaceSpec] = {
    "generic": ApiSurfaceSpec(name="generic"),
    "hloc": ApiSurfaceSpec(
        name="hloc",
        expected_actions=HLOC_EXPECTED_ACTIONS,
        forbidden_actions=HLOC_FORBIDDEN_ACTIONS,
        forbidden_prefixes=("hloc.pipeline",),
    ),
}
