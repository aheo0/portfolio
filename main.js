var form_validator = new Validator("contacts_form");
form_validator.addValidation("name","req","Please provide your name");
form_validator.addValidation("email","req","Please provide your email");
form_validator.addValidation("email","email","Please enter a valid email address");
form_validator.addValidation("website_poll","selone_radio");
form_validator.addValidation("comments","req");

function validate_form() {
    return true;
}