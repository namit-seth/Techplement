function del(task_id){
    let form_id = "form_del_".concat(task_id);
    form = document.getElementById(form_id);
    form.submit();
    // console.log(form);
}
// <button class="task_action" onclick="edit('{{ i[0] }}')"><i class="fa-regular fa-pen-to-square fa-xl"></i></button>
function save(task_id){
    let form_id = "form_edit_".concat(task_id);
    let input_id = "edit_".concat(task_id);
    let input = document.getElementById(input_id);
    input.value = document.getElementById(task_id).textContent;
    form = document.getElementById(form_id);
    form.submit();
    // console.log(form);
}
function edit(task_id){
    let task = document.getElementById(task_id);
    task.contentEditable = "true";
    let button = document.createElement("button");
    button.classList = ["task_action"];
    button.onclick = function() {save(task_id)};
    button.innerHTML = '<i class="fa-regular fa-floppy-disk fa-xl"></i>';
    let icons_id = "icons_".concat(task_id);
    icons = document.getElementById(icons_id)
    icons.insertBefore(button, icons.children[0]);
}