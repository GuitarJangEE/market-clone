const getWriteForm = document.getElementById("write-form");
const eng = document.getElementById("eng");

const handleSubmit = async (submitStop) => {
  submitStop.preventDefault();
  const bodyAddTime = new FormData(getWriteForm);
  bodyAddTime.append("insertAT", new Date().getTime());
  try {
    bonem = await fetch("/items", {
      method: "POST",
      body: bodyAddTime,
    });
    const ch = await bonem.json();
    if (ch === "200") {
      window.location.pathname = "/";
    }
  } catch (g) {
    console.error(g);
  }
  //   console.log("뿌앵");
};
const engd = async (submitStop) => {
  submitStop.preventDefault();
  const bodyAddTime = new FormData(eng);
  bodyAddTime.append("insertAT", new Date().getTime());
  try {
    serverro = await fetch("/itemss", {
      method: "POST",
      body: bodyAddTime,
    });
    const info = await serverro.json();
    if (info === "시후") {
      window.location.pathname = "/";
    }
  } catch (e) {
    console.error(e);
  }
  //   console.log("앵");
};

getWriteForm.addEventListener("submit", handleSubmit);
eng.addEventListener("submit", engd);
