const form = document.querySelector('#task-form');
const titleInput = document.querySelector('#task-title');
const list = document.querySelector('#tasks');
const statusEl = document.querySelector('#status');

function status(text, error = false) {
  statusEl.textContent = text;
  statusEl.classList.toggle('error', error);
}

async function loadTasks() {
  try {
    const res = await fetch('/api/tasks');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const tasks = await res.json();
    list.replaceChildren();
    for (const task of tasks) {
      const li = document.createElement('li');
      li.textContent = `#${task.id} — ${task.titulo}`;
      list.appendChild(li);
    }
    status(`${tasks.length} tarefa(s) carregada(s).`);
  } catch (err) {
    status(`Não foi possível buscar as tarefas (${err.message}).`, true);
  }
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const titulo = titleInput.value.trim();
  if (!titulo) return;
  try {
    const res = await fetch('/api/tasks', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({titulo}),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    titleInput.value = '';
    await loadTasks();
  } catch (err) {
    status(`Não foi possível gravar a tarefa (${err.message}).`, true);
  }
});

loadTasks();
