
fetch('../profiles/tissue_types_v1.json')
    .then(response => response.json())
    .then(data => {
        const tissue_types = data;

        // Rename 'NAME' to 'text' and remove unwanted fields
        function renameKeys(obj) {
            if (Array.isArray(obj)) {
                return obj.map(renameKeys);
            } else if (obj !== null && typeof obj === 'object') {
                let renamedObj = {};
                for (let key in obj) {
                    if (key === "name") {
                        renamedObj["text"] = renameKeys(obj[key]);
                    } else {
                        renamedObj[key] = renameKeys(obj[key]);
                    }
                }
                return renamedObj;
            } else {
                // not an object or array, so just return the value
                return obj;
            }
        }
        function pruneKeys(obj) {
            if (Array.isArray(obj)) {
                return obj.map(pruneKeys);
            } else if (obj !== null && typeof obj === 'object') {
                let prunedObj = {};
                for (let key in obj) {
                    if (key === "NAME" || key === "text" || key === "children") {
                        prunedObj[key] = pruneKeys(obj[key]);
                    }
                }
                return prunedObj;
            } else {
                // not an object or array, so just return the value
                return obj;
            }
        }

        $(function() {
            const tissue_types_renamed = renameKeys(tissue_types);
            const tissue_types_pruned = pruneKeys(tissue_types_renamed)
            // tissue_types_pruned[0]['icon'] = 'static/images/endocrine-system.png'
            $('#jstree_demo').jstree({ // config object start
                "core": {                    // core config object
                    "mulitple": false,         // disallow multiple selection
                    "animation": 100,          // 200ms is default value
                    "check_callback" : true,   // this make contextmenu plugin to work
                    "themes": {
                        "variant": "medium",
                        "dots": false
                    },
                    "data":
                    tissue_types_pruned
                    // data core options end

                },

                // Types plugin
                "types" : {
                    "default" : {
                        "icon" : "glyphicon glyphicon-flash"
                    },
                    "demo" : {
                        "icon" : "glyphicon glyphicon-th-large"
                    }
                },

                // config object for Checkbox plugin (declared below at plugins options)
                "checkbox": {
                    "keep_selected_style": false,  // default: false
                    "three_state": true,           // default: true
                    "whole_node": true             // default: true
                },

                "conditionalselect" : function (node, event) {
                    return false;
                },

                // injecting plugins
                "plugins" : [
                    // "dnd",
                    // "massload",
                    // "search",
                    // "sort",
                    // "state",
                    "types",
                    // Unique plugin has no options, it just prevents renaming and moving nodes
                    // to a parent, which already contains a node with the same name.
                    "unique",
                    // "wholerow",
                    // "conditionalselect",
                    "changed"
                ]
            }); // config object end

            // AJAX loading JSON Example:
            $('#jstree_ajax_demo').jstree({
                'core': {
                    'data': {
                        "url" : "https://codepen.io/stefanradivojevic/pen/dWLZOb.js",
                        "dataType" : "json" // needed only if you do not supply JSON headers
                    }
                },
                // Types plugin
                "types" : {
                    "default" : {
                        "icon" : "glyphicon glyphicon-record"
                    }
                },
                "plugins" : [ "types", "unique" ]
            });

            // Listen for events - example
            $('#jstree_demo_div').on("changed.jstree", function (e, data) {
                // changed.jstree is a event
                // console.log(data.selected);
                console.log('ds: ' + data.changed.deselected);
            });

        });
    });
