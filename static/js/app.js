var board = null
var game = new Chess()

setTimeout(function() {
  board = Chessboard('board2', config)
  $('#startBtn').on('click', game.start)
  $('#clearBtn').on('click', game.clear)
}, 0);

function onDragStart (source, piece, position, orientation) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false

  // only pick up pieces for White
  if (piece.search(/^b/) !== -1) return false
}

function makeRandomMove () {
  var fen = game.fen()
  $.get("http://127.0.0.1:5000/api/v1/suggest_move?fen=" + fen, function(data) {
        console.log("lol")
        console.log(data)
        game.move(data, {sloppy: true});
        //updateStatus();
        // The animations would stutter when moves were returned too quick, so I added a 100ms delay before the animation
        board.position(game.fen());
    })
  // game over
}

function onDrop (source, target) {
  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  })

  // illegal move
  if (move === null) return 'snapback'

  // make random legal move for black
  window.setTimeout(makeRandomMove, 250)
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd () {
  board.position(game.fen())
}

var config = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
}