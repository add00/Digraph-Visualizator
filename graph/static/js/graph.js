var cells = [];
var nodes = [];

(function(){;
    loadGraph();
    $('[data-toggle="tooltip"]').tooltip()
})();


var graph = new joint.dia.Graph;
var selectedGraphID = 1;

/*
 * Prepares canvas for new selected graph.
 */
function clearGraphOnLoad() {
    graph.clear();
    $('#paper-restrict').empty()
}

/*
 * Loads graph.
 */
function loadGraph() {
    selectedGraphID = $("#id_graph").val();
    $.ajax({
        type: 'GET',
        url: '/api/v1/graph/' + selectedGraphID,
        error: function(data){
            displayErrorMessage('error-message', 'Have you selected a graph?', false);
        },
        success: function(data){
            clearGraphOnLoad();
            ajaxCallBack(data);
            cells = [];
            $('#error-message').hide();
        }
    });
}

/*
 * CallBack on succeed response from Graph API.
 */
function ajaxCallBack(data){
    graph = new joint.dia.Graph;
    graph.cid = data.pk;
    nodes = data.nodes;
    var paper = new joint.dia.Paper({
        el: $('#paper-restrict'),
        width: 1140, height: 650, gridSize: 1,
        model: graph,
        defaultLink: new joint.dia.Link({
            attrs: {'.marker-target': {d: 'M 10 0 L 0 5 L 10 10 z'}}
        }),
        snapLinks: {radius: 75},
        validateConnection: function(cellViewS, magnetS, cellViewT, magnetT, end, linkView) {
            if (magnetS && magnetS.getAttribute('type') === 'input') return false;
            if (cellViewS === cellViewT) return false;
            return magnetT && magnetT.getAttribute('type') === 'input';
        },
        validateMagnet: function(cellView, magnet) {
            return magnet.getAttribute('magnet') !== 'passive';
        }
    });

    $.each(nodes, function(index, value) {
        var m = new joint.shapes.devs.Model({
            position: { x: value.x, y: value.y },
            size: { width: 90, height: 90 },
            id: value.uuid,
            inPorts: ['in'],
            outPorts: ['out'],
            remove: true,
            attrs: {
                '.label': {text: value.index, 'ref-x': .5, 'ref-y': .4},
                rect: {fill: '#337ab7'},
                '.inPorts circle': {fill: '#EEE', magnet: 'passive', type: 'input'},
                '.outPorts circle': {fill: '#222', type: 'output'}
            }
        });
        cells.push(m);
    });

    $.each(nodes, function(index, value) {
        var uuid = value.uuid;
        $.each(value.arcs, function(index, arc) {
            var l = new joint.shapes.devs.Link({
                source: { id: uuid, port: 'out' },
                target: { id: arc, port: 'in' },
                attrs: { '.marker-target': { d: 'M 10 0 L 0 5 L 10 10 z' } }
            });
            cells.push(l);
        });
    });
    graph.addCell(cells);
}

/*
 * Updates graph.
 */
function updateGraph() {
    var arcs = graph.getLinks();
    var elements = graph.getElements();
    var graphId = graph.cid;
    var numberOfArcs = 0;
    var numberOfNodes = 0;
    var sendData = [];

    $.each(elements, function(key, vertex) {
        sendData.push({name: "node-" + key + "-uuid", value: vertex.id});
        sendData.push({name: "node-" + key + "-graph", value: graphId});
        sendData.push({name: "node-" + key + "-x", value: vertex.position().x});
        sendData.push({name: "node-" + key + "-y", value: vertex.position().y});
        numberOfNodes++;
    });
    sendData.push({name: 'node-TOTAL_FORMS', value: numberOfNodes});
    sendData.push({name: 'node-INITIAL_FORMS', value: numberOfNodes});
    sendData.push({name: 'node-MIN_NUM_FORMS', value: 0});
    sendData.push({name: 'node-MAX_NUM_FORMS', value: 1000});

    $.each(graph.getLinks(), function(key, arc) {
            sendData.push({name: "arc-" + key + "-index_from", value: arc.attributes.source.id});
            sendData.push({name: "arc-" + key + "-index_to", value: arc.attributes.target.id});
            numberOfArcs++;
    });
    sendData.push({name: 'arc-TOTAL_FORMS', value: numberOfArcs});
    sendData.push({name: 'arc-INITIAL_FORMS', value: numberOfArcs});
    sendData.push({name: 'arc-MIN_NUM_FORMS', value: 0});
    sendData.push({name: 'arc-MAX_NUM_FORMS', value: 1000});

    sendData.push({name: 'csrfmiddlewaretoken', value: $("input[name='csrfmiddlewaretoken']").val()});
    debugger;
    $.ajax({
        type: 'POST',
        url: '/api/v1/arc/' + selectedGraphID,
        data: sendData,
        error: function(data){
            displayErrorMessage('error-message', 'Oops... something went wrong', false);
        },
        success: function(data){
            displayErrorMessage('error-message', 'Changes have been saved', true);
            window.location.replace('/graph/' + selectedGraphID);
        }
    });
}


/**
 * Removes graph or vertex basing on form.
 */
function removeGraphOrNode() {
    var graphID = $("#id_graph").val();
    var sendData = [];
    var nodeIndex = $("#id_index").val();

    sendData.push({name: 'csrfmiddlewaretoken', value: $("input[name='csrfmiddlewaretoken']").val()});

    if (!nodeIndex) {
        $.ajax({
            type: 'POST',
            url: '/remove/graph/' + graphID,
            data: sendData,
            error: function(data){
                debugger;
                displayErrorMessage('error-message', 'Oops... something went wrong', false);
            },
            success: function(data){
                displayErrorMessage('error-message', 'Graph has been removed', true);
                window.location.replace('/');
            }
        });
    } else {
        $.ajax({
            type: 'POST',
            url: '/remove/node/' + nodeIndex + '?graph=' + graphID,
            data: sendData,
            error: function(data){
                displayErrorMessage('error-message', 'Oops... node does not exist', false);
            },
            success: function(data){
                displayErrorMessage('error-message', 'Node has been removed', true);
                window.location.replace('/graph/' + graphID);
            }
        });
    }

}

/**
 * Handles saving files.
 */
function saveToFile(data, fileName) {
    var fileData = new Blob([data], {type:'text/plain'});
    var fileName = fileName + '.json';
    var link = document.createElement("a");

    window.URL = window.URL || window.webkitURL;

    link.download = fileName;
    link.href = window.URL.createObjectURL(fileData);
    link.onclick = destroyLink;
    link.style.display = "none";
    document.body.appendChild(link);

    link.click();
}

/**
 * Destroys not longer needed link from DOM.
 */
function destroyLink(event)
{
    document.body.removeChild(event.target);
}

/**
 * Graph data serializer.
 */
function getSerializedGraph() {
    $.ajax({
        type: 'GET',
        url: '/api/v1/graphs/',
        error: function(data){
            displayErrorMessage('error-message', 'Oops... something went wrong', false);
        },
        success: function(data){
            var jsonData = JSON.stringify(data);
            var inputFileName = $('#file-name').val();
            var fileName = (inputFileName !== '') ? inputFileName : 'graphs';

            saveToFile(jsonData, fileName);
            displayErrorMessage('error-message', 'Data saved', true);
        }
    });
}

/**
 * Displays error message.
 */
function displayErrorMessage(id, message, success) {
    var _class = "left-padding alert alert-danger";
    var sign = "glyphicon glyphicon-exclamation-sign";
    if (success) {
        _class = "left-padding alert alert-success";
        sign = "glyphicon glyphicon-ok-sign";
    }
    var errors = $("#" + id)
        .css("visibility", "visibile")
        .attr("class", _class)
        .empty()
        .show();

    var errorSign = $('<span></span>')
        .addClass(sign)
        .attr('aria-hidden', true);

    var errorMessage = $('<span></span>')
        .text(message);

    errors.append(errorSign);
    errors.append(errorMessage);
}
