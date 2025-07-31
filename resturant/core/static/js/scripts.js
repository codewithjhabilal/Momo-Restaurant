const input = document.querySelector("#phone");
const error_msg=document.getElementById("error_msg");
const ho=window.intlTelInput(input, {
  initialCountry: "NP",
  strictMode: true,
  loadUtils: () => import("https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/25.3.1/build/js/utils.js") // for formatting/placeholders etc
});

document.getElementById('contactForm').addEventListener('submit',function(e){
  if(ho.isValidNumber()){
    input.value=ho.getNumber();
    error_msg.style.display='none'
  }
  else{
    e.preventDefault();
    error_msg.style.display='inline'
  }
})