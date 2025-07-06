document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("formset-container");
  const addBtn = document.getElementById("add-choice-button");
  const removeBtn = document.getElementById("remove-choice-button");
  const totalForms = document.getElementById("id_choice_set-TOTAL_FORMS");

  addBtn.addEventListener("click", function () {
    const currentFormCount = parseInt(totalForms.value);
    const existingForm = container.querySelector("div.formset-form");

    const newForm = existingForm.cloneNode(true);

    newForm.querySelectorAll("input, label").forEach((el) => {
      // update name
      if (el.name) {
        el.name = el.name.replace(/choice_set-(\d+)-/, `choice_set-${currentFormCount}-`);
      }
      // update id
      if (el.id) {
        el.id = el.id.replace(/id_choice_set-(\d+)-/, `id_choice_set-${currentFormCount}-`);
      }
      // reset values
      if (el.tagName === "INPUT") {
        if (el.type === "text" || el.type === "hidden") el.value = "";
        if (el.type === "checkbox") el.checked = false;
      }
      // update label for=
      if (el.htmlFor) {
        el.htmlFor = el.htmlFor.replace(/id_choice_set-(\d+)-/, `id_choice_set-${currentFormCount}-`);
      }
    });

    container.appendChild(newForm);
    totalForms.value = currentFormCount + 1;
  });

  removeBtn.addEventListener("click", function () {
    const forms = container.querySelectorAll(".formset-form");
    if (forms.length > 1) {
      forms[forms.length - 1].remove();
      totalForms.value = forms.length - 1;
    }
  });
});
