/* Form */
var submitted = false;
function form_thank_you () {
    submitted = true;
    document.getElementById('gform').style.display = 'none';
    document.getElementById('thank_you4form').style.display = 'initial';
    document.getElementById('thank_you4form').style.display = 'block';
    document.getElementById('form_info').style.display = 'none';
}