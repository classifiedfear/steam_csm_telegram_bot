pattern_list = {
    "operationName": "pattern_list",
    "variables": {
        "name": "",
        "exterior": "",
        "sortBy": "float_value"
    },
    "query": "query pattern_list("
             "$contains_paint_seed: Int, $exterior: String, $name: String!, $rareOnly: Boolean, $sortBy: String"
             ") {"
             "\n  pattern_list(\n    input: {"
             "contains_paint_seed: $contains_paint_seed, "
             "exterior: $exterior, "
             "name: $name, "
             "rare_only: $rareOnly, "
             "sort_by: $sortBy}\n  "
             ") {"
             "\n    available\n    exterior\n    float_value\n    paint_seed\n    rare_name\n    uuid\n  }\n"
             "}"
}

get_min_available = {
    "operationName": "get_min_available",
    "variables": {"name": ""},
    "query": "query get_min_available("
             "$name: String!) {\n  get_min_available(name: $name"
             ") {"
             "\n    name\n"
             "isSouvenir\n"
             "isStatTrack\n    "
             "bestPrice\n    "
             "bestSource\n"
             "source {\n      "
             "trade {\n        "
             "lowestPrice\n        "
             "count\n      "
             "}\n      market {\n        lowestPrice\n        count\n      }\n    }\n  }\n}"}
