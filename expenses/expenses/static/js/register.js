const usernameField=document.querySelector("#usernameField");
const feedbackArea = document.querySelector(".invalid_feedback")
const emailFeedbackArea = document.querySelector(".email_invalid_feedback");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailField = document.querySelector("#emailField");
const submitButton = document.querySelector("#submit_button");

const showPasswordToggle = document.querySelector(".showPasswordToggle");
const passwordField = document.querySelector("#passwordField");


showPasswordToggle.addEventListener("click", (e) => {
    if (showPasswordToggle.textContent==="SHOW")
    {
        showPasswordToggle.textContent = "HIDE"; 
        passwordField.setAttribute("type", "text");
    }
    else 
    {
        showPasswordToggle.textContent = "SHOW"; 
        passwordField.setAttribute("type", "password"); 
    }
});



emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value; 
    emailField.classList.remove("is-invalid"); 
    emailFeedbackArea.style.display = "none";  
    if (emailVal.length > 0)
    {
        fetch('/authentication/validate_email', {
            body: JSON.stringify({email: emailVal}), 
            method: "POST", 
        }).then(res => res.json())
        .then(data => {
            if (data.email_error) {
                // disable submit button 
                submitButton.disabled=true;
                emailField.classList.add("is-invalid"); 
                emailFeedbackArea.innerHTML=`<p>${data.email_error}</p>`;
                emailFeedbackArea.style.display = "block";  
            }
            else 
            {
                submitButton.removeAttribute("disabled");
            }
        });
    }
});



usernameField.addEventListener("keyup", (e) => {

    const usernameVal = e.target.value;  // This contains the value of what user types. 
    usernameSuccessOutput.style.display = "block"; 
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;
    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display = "none"; 
    if (usernameVal.length > 0) {
        fetch('/authentication/validate_username', {

        body: JSON.stringify({username: usernameVal}), 
        method:'POST',
        })
        .then((res) => res.json())
        .then((data)=>{
            usernameSuccessOutput.style.display = "none"; 
            if (data.username_error) {
                submitButton.disabled=true; 
                usernameField.classList.add("is-invalid");
                feedbackArea.innerHTML=`<p>${data.username_error}</p>`;
                
                feedbackArea.style.display = "block";  
            }
            else 
            {
                submitButton.removeAttribute('disabled');
            }
        });
    }
}); 