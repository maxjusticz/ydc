var peer = null;
var conn = null;

$("#login").click(function() {
    peer = new Peer($("#me").val(), {key: '3ks42vh9k4jthuxr'});
    console.log(peer);
    peer.on('connection', function(conn) {
	conn.on('data', function(data){
	    console.log(data);
	});
    });
});

$("#pair").click(function() {
    initiate_conn($("#peer").val());
});

function initiate_conn(peername) {
    conn = peer.connect(peername);
    conn.on('open', function(){
	console.log('conn open');
	conn.send('HELO');
    });
}
