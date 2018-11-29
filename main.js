/* Form */
document.getElementById('thank_you4form').style.display = 'none';
var submitted = false;
function form_thank_you () {
    submitted = true;
    document.getElementById('gform').style.display = 'none';
    document.getElementById('thank_you4form').style.display = 'visible';
}