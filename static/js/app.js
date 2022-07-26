var board = null
var game = new Chess()
var startFen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  // This is a starting position
var side = 'b'
setTimeout(function() {
  board = Chessboard('board2', config)
  $('#startBtn').on('click', startgame)
  $('#clearBtn').on('click', board.clear)
  $('#swapBtn').on('click', flip)
}, 0);

// This function starts the board
function startgame(){
  board.position(startFen)
  game.reset()
  board.start()
}

// Flips the board and makes a move
function flip(){
  board.flip()
  side = 'w'
  window.setTimeout(makeMove, 250)
}


function onDragStart (source, piece, position, orientation) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false

  // only pick up pieces for White
  if (piece.search(/^${side}/) !== -1) return false
}

// This Function calls our server's api for a move
function makeMove () {
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

// This function is responsible for the process of making a move
// If the move is not legal, it won't allow it
// If it's legal it call function makeMove
function onDrop (source, target) {
  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  })

  // illegal move
  if (move === null) return 'snapback'

  // make move
  window.setTimeout(makeMove, 250)
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