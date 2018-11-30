/* NavBar 
-- supposed to tell user what each navbar image represents --
might use data-tooltip in the future;
might create own boxes to put information;
might keep current design w/o "tooltip"'s
*jQuery is needed for the script below
$("a").hover(function(e) {
        $($(this).data("tooltip")).css({
            left: e.pageX + 10,
            top: e.pageY + 3,
            display: initial
        }).stop();
    }
    function() {
        $($(this).data("tooltip")).css({
            display: hidden;
        }).stop();
    });*/

/* Form */
var submitted = false;
function form_thank_you () {
    submitted = true;
    document.getElementById('gform').style.display = 'none';
    document.getElementById('thank_you4form').style.display = 'block';
    document.getElementById('form_info').style.display = 'none';
}