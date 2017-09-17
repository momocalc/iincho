
function buildTreeview(treeData) {
    var success_drop;
    $('#treeview').treeview({
            data: treeData,
            onTreeRendered: function () {

                var $draggable_node;
                var node_height = 40;
                var margin = 7;
                var state;

                function reset_state() {
                    state = null;
                    change_state();
                    $draggable_node = null;
                }

                /*
                 * ドラッグの状態変化
                 * stateを変更する(above/below/child)
                 */
                function change_state() {
                    if (!$draggable_node) return;

                    $draggable_node.removeClass('draggable-above')
                        .removeClass('draggable-below')
                        .removeClass('ui-state-hover');

                    if (state) {
                        if (state === 'above') {
                            $draggable_node.addClass('draggable-above');
                        } else if (state === 'below') {
                            $draggable_node.addClass('draggable-below');
                        } else if (state === 'child') {
                            $draggable_node.addClass('ui-state-hover');
                        }
                    }
                }

                /**
                 * jQueryIOでドラッグ可能にする
                 */
                $('#treeview .list-group-item').draggable({
                    stack: '.drag',
                    zIndex: 10,
                    opacity: 0.7,
                    revert: function (event, ui) {
                        reset_state();
                        return !event || !success_drop;
                    }
                    , drag: function (event, ui) {
                        if (!$draggable_node) {
                            return;
                        }
                        var distance = $(this).position().top - $draggable_node.position().top;
                        distance += node_height / 2;

                        if (distance < margin) {
                            state = 'above';
                        } else if (distance > node_height - margin) {
                            state = 'below';
                        } else if (margin <= distance && distance <= node_height) {
                            state = 'child';
                        } else {
                            state = null;
                        }
                        change_state();
                    }
                });

                //ドロップオブジェクト設定
                $('#treeview .list-group-item, #treeview .drop_margin').droppable({
                    over: function (event, ui) {
                        reset_state();
                        $draggable_node = $(this);
                    },
                    drop: function (event, ui) {
                        var dragged_node = $(ui['draggable'][0]);
                        var dropped_node = $(this);
                        success_drop = 'success' === $('#treeview').treeview('moveNode', [dragged_node.data('nodeid'),
                                dropped_node.data('nodeid'), state]);
                    }
                });
                $('.treeview-container').droppable({
                    drop: function (event, ui) {
                        if (!state) {
                            return;
                        }
                        var dragged_node = $(ui['draggable'][0]);
                        var dropped_node = $draggable_node;
                        if (dragged_node && dropped_node) {
                            success_drop = 'success' === $('#treeview').treeview('moveNode', [dragged_node.data('nodeid'),
                                    dropped_node.data('nodeid'), state]);
                        } else {
                            success_drop = false;
                        }
                    }
                });
            }
        }
    );
}


/* -- 追加/削除 -- */
function add_node() {
    var nodes = $('#treeview1').treeview('getSelected');
    var new_node = {
        text: $('#input-add').val() ? $('#input-add').val() : 'new node',
        href: '#'
    };
    if (nodes.length > 0) {
        $('#treeview1').treeview('addNode', [new_node, nodes[0].nodeId]);
    } else {
        $('#treeview1').treeview('addNode', [new_node]);
    }
}

function remove_node() {
    var nodes = $('#treeview1').treeview('getSelected');
    if (nodes.length > 0) {
        $('#treeview1').treeview('removeNode', [nodes[0].nodeId]);
    }
}

/* -- edit text -- */
function edit_text() {
    var nodes = $('#treeview1-2').treeview('getSelected');
    var new_text = $('#input-edit').val() ? $('#input-edit').val() : 'new text';
    if (nodes.length > 0) {
        $('#treeview1-2').treeview('setText', [nodes[0].nodeId, new_text]);
    }
}

/* -- dropdown -- */
function selected_dd_item(e) {
    console.log();
    var txt = e.data['node']['text'] + ' - ' + e.data['item_text'] + ' clicked';
    $('#dd_event').append($('<p></p>').html(txt));
}

