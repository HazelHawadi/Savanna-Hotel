(function () {
    emailjs.init({
        publicKey: "I-EySgIfyHnjJUejh",
    });
})();

// Function to send email
function sendEmail(contactForm) {
    emailjs.send("service_sxfnd9dg", "template_1o2cx1c", {
        "name": contactForm.name.value,
        "email": contactForm.email.value,
    })
    .then(
        function(response) {
            console.log("SUCCESS", response);
        },
        function(error) {
            console.log("FAILED", error);
        }
    );
    return false;  // To block from loading a new page
}