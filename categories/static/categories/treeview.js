/**
 * カテゴリ操作のヘルパー
 * @param $treeView treeView JQ Object
 * @param treeData
 * @constructor
 */
var TreeViewHelper = function ($treeView, treeData) {
    var _this = this;

    /**
     * Event handlers
     */
    this.handler = {
        onMovingNode: function () {
            return true;
        },
        onMovedNode: function () {
            return true;
        },
        onClickedDeleteNode: function () {
        },
        onClickedUpdateName: function () {
        },
        onClickedAddChild: function () {
        }
    };

    var addChildMenuItem = {
        key: 'addChild',
        text: '子カテゴリ追加',
        action: clickedDropDownButton
    };
    var dropdownMenuItems = [
        {
            key: 'updateName',
            text: '名称変更',
            action: clickedDropDownButton
        }, addChildMenuItem,
        "divider",
        {
            key: 'delete',
            text: '削除',
            action: clickedDropDownButton
        }
    ];

    function addDropDownMenu(node) {
        node.dropdown = jQuery.extend(true, {}, dropdownMenuItems);
        if (node.hasOwnProperty('nodes')) {
            node.nodes.forEach(addDropDownMenu);
        }
    }

    /**
     * wrap treeview
     * @returns {*}
     */
    this.treeview = function () {
        return $treeView.treeview.apply($treeView, arguments);
    };

    /**
     * 指定ノードのパスを構成し返却する
     * @param node
     * @returns {string}
     */
    this.getPath = function (node) {
        var path = '';
        while (node['parentId'] !== undefined) {
            path = node.name + '/' + path;
            node = $treeView.treeview('getParent', node.nodeId);
        }
        return path;
    };

    function build() {
        var isSuccessDropped; // ドロップでの移動成功フラグ

        // ドロップダウンメニューの追加
        treeData.forEach(addDropDownMenu);
        /**
         * ノードデータをラッピング
         * トップ(根)には"root"を表示する
         */
        var tree = {
            text: "root",
            name: "",
            nodes: treeData,
            dropdown: [addChildMenuItem] // rootは子追加のメニューアイテムのみ表示
        };

        $treeView.treeview({
                data: [tree],
                levels: 3,
                highlightSelected: false,
                showCheckbox: true,
                onTreeRendered: function () {
                    var $draggableNode;
                    var nodeHeight = 40;
                    var margin = 1;
                    var state;

                    function reset_state() {
                        state = null;
                        change_state();
                        $draggableNode = null;
                    }

                    /*
                     * ドラッグの状態変化
                     * stateを変更する(above/below/child)
                     */
                    function change_state() {
                        if (!$draggableNode) return;

                        $draggableNode.removeClass('draggable-above')
                            .removeClass('draggable-below')
                            .removeClass('ui-state-hover');

                        if (state) {
                            if (state === 'above') {
                                $draggableNode.addClass('draggable-above');
                            } else if (state === 'below') {
                                $draggableNode.addClass('draggable-below');
                            } else if (state === 'child') {
                                $draggableNode.addClass('ui-state-hover');
                            }
                        }
                    }

                    /**
                     * jQueryIOでドラッグ可能にする
                     */
                    $treeView.find('.list-group-item:not(:first-child)').draggable({
                        stack: '.drag',
                        zIndex: 10,
                        opacity: 0.7,
                        revert: function (event, ui) {
                            reset_state();
                            return !event || !isSuccessDropped;
                        }
                        , drag: function (event, ui) {
                            if (!$draggableNode) {
                                return;
                            }
                            var distance = $(this).position().top - $draggableNode.position().top;
                            distance += nodeHeight / 2;

                            // このスクリプトでは子へのドロップしか許容しない
                            if (margin <= distance && distance <= nodeHeight) {
                                state = 'child';
                            } else {
                                state = null;
                            }
                            change_state();
                        }
                    });

                    //ドロップオブジェクト設定
                    $treeView.find('.list-group-item').droppable({
                        over: function (event, ui) {
                            reset_state();
                            $draggableNode = $(this);
                        },
                        drop: function (event, ui) {

                            var draggedNodeId = $(ui['draggable'][0]).data('nodeid');
                            var droppedNodeId = $(this).data('nodeid');

                            //移動前通知(falseが帰ってきた場合は、中断)
                            if (!_this.handler.onMovingNode(
                                    _this.treeview('getNode', draggedNodeId),
                                    _this.treeview('getNode', droppedNodeId))
                            ) {
                                isSuccessDropped = false;
                                return;
                            }
                            isSuccessDropped = 'success' === _this.treeview('moveNode',
                                    [draggedNodeId, droppedNodeId, state]);

                            if (isSuccessDropped) {
                                // 移動後通知
                                _this.handler.onMovedNode(
                                    _this.treeview('getNode', draggedNodeId),
                                    _this.treeview('getNode', droppedNodeId));
                            }
                        }
                    });

                    // rootのcheckboxは表示しない
                    $treeView.find('.check-icon:first').hide();
                }
            }
        );
    }

    build();

    function clickedDropDownButton(e) {
        if (e.data.item_key === 'delete') {
            _this.handler.onClickedDeleteNode(e.data.node);
        } else if (e.data.item_key === 'updateName') {
            _this.handler.onClickedUpdateName(e.data.node);
        } else if (e.data.item_key === 'addChild') {
            _this.handler.onClickedAddChild(e.data.node);
        }
    }

    this.deleteNode = function (node) {
        var nodeId = node.nodeId;
        _this.treeview('removeNode', nodeId);
    };

    this.updateNodeName = function (node, name) {
        var nodeId = node.nodeId;
        node.name = name;
        var escapedName = $('<span/>').text(name).html();
        _this.treeview('setText', [nodeId, escapedName]);
    };

    this.addNode = function (parentNode, name) {
        var escapedName = $('<span/>').text(name).html();
        var node = {
            text: escapedName,
            name: name
        };
        addDropDownMenu(node);
        _this.treeview('addNode', [node, parentNode.nodeId]);
        _this.treeview('expandNode', parentNode.nodeId);
    }

    this.updateNodeName = function(node, name){
        var nodeId = node.nodeId;
        node.name = name;
        _this.treeview('setText',[nodeId, name] );
    }

};
