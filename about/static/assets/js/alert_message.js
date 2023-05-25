const toast = document.querySelector(".toast");
const closeIcon = document.querySelector(".close");
const progress = document.querySelector(".progress");

let timer1, timer2;

// Function to show the toast message
const showToast = () => {
  toast.classList.add("active");
  progress.classList.add("active");

  timer1 = setTimeout(() => {
    toast.classList.remove("active");
  }, 5000);

  timer2 = setTimeout(() => {
    progress.classList.remove("active");
  }, 5300);
};

// Function to hide the toast message
const hideToast = () => {
  toast.classList.remove("active");
  setTimeout(() => {
    progress.classList.remove("active");
  }, 300);

  clearTimeout(timer1);
  clearTimeout(timer2);
};

// Show the toast message on page load
showToast();

// Event listener for close icon click
closeIcon.addEventListener("click", () => {
  hideToast();
});