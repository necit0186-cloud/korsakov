const ICONS = {
  grid: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>',
  file: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 12h6M9 16h6"/></svg>',
  chart: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
  link: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M10 13a5 5 0 0 0 7.1.1l2-2a5 5 0 0 0-7-7.1l-1.1 1M14 11a5 5 0 0 0-7.1-.1l-2 2A5 5 0 0 0 12 20l1.1-1"/></svg>',
  sparkles: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m12 3 1.3 3.7L17 8l-3.7 1.3L12 13l-1.3-3.7L7 8l3.7-1.3L12 3ZM19 14l.8 2.2L22 17l-2.2.8L19 20l-.8-2.2L16 17l2.2-.8L19 14ZM5 12l.8 2.2L8 15l-2.2.8L5 18l-.8-2.2L2 15l2.2-.8L5 12Z"/></svg>',
  dots: '<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="5" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="19" cy="12" r="1.5"/></svg>',
  calendar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></svg>',
  chevron: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m7 10 5 5 5-5"/></svg>',
  refresh: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 7v5h-5M4 17v-5h5"/><path d="M6.1 8A7 7 0 0 1 18.5 6L20 12M4 12l1.5 6A7 7 0 0 0 18 16"/></svg>',
  bell: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9ZM10 21h4"/></svg>',
  menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
  users: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/></svg>',
  eye: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>',
  heart: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.8-7.5 1.1-1.1a5.5 5.5 0 0 0-.1-7.8Z"/></svg>',
  layers: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m12 2 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5M3 17l9 5 9-5"/></svg>',
  arrowUp: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m18 15-6-6-6 6"/></svg>',
  bulb: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 18h6M10 22h4M8.2 15.2A7 7 0 1 1 15.8 15c-.8.6-.8 1.5-.8 2H9c0-.5 0-1.3-.8-1.8Z"/></svg>',
  clock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
  target: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></svg>',
  download: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>',
  search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>',
  plus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>',
  shield: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/></svg>',
  check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 12 4 4L19 6"/></svg>',
  alert: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v6M12 17h.01"/></svg>',
};

const state = {
  period: 30,
  metric: 'audience',
  dashboard: null,
  contentPlatform: 'all',
  search: '',
  sortDesc: true,
  authenticated: false,
  account: null,
  cabinet: null,
  folderId: null,
  folders: [],
  sharedFolders: [],
  ownedFolders: [],
  folderLimit: 1,
  archiveYear: new Date().getUTCFullYear() - 1,
};

const platformLabels = { vk: 'ВКонтакте', telegram: 'Telegram', max: 'MAX' };
const platformLetters = { vk: 'VK', telegram: 'T', max: 'M' };
const number = new Intl.NumberFormat('ru-RU');
const compact = new Intl.NumberFormat('ru-RU', { notation: 'compact', maximumFractionDigits: 1 });

function icon(name) { return ICONS[name] || ''; }
function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>'"]/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#039;', '"': '&quot;' }[char]));
}
function formatNumber(value) { return number.format(Math.round(Number(value) || 0)); }
function formatCompact(value) {
  const v = Number(value) || 0;
  if (v >= 1_000_000) return `${(v / 1_000_000).toFixed(1).replace('.', ',')} млн`;
  if (v >= 1_000) return `${(v / 1_000).toFixed(v >= 100_000 ? 0 : 1).replace('.', ',')} тыс.`;
  return formatNumber(v);
}
function formatKpi(item) {
  if (item.format === 'percent') return `${String(item.value).replace('.', ',')}%`;
  if (item.format === 'compact') return formatCompact(item.value);
  return formatNumber(item.value);
}

function hydrateIcons(root = document) {
  root.querySelectorAll('[data-icon]').forEach(node => {
    const name = node.dataset.icon;
    if (ICONS[name]) node.innerHTML = ICONS[name];
  });
}

async function api(path, options) {
  const response = await fetch(path, options);
  const data = await response.json().catch(() => ({}));
  if (response.status === 401 && !path.startsWith('/api/auth/')) showAuth(false);
  if (!response.ok) throw new Error(data.error || 'Ошибка запроса');
  return data;
}

function initials(name) {
  return String(name || 'Пользователь').split(/\s+/).filter(Boolean).slice(0, 2).map(word => word[0]).join('').toLocaleUpperCase('ru') || '—';
}

function applyAccount(account) {
  state.account = account;
  if (!account) return;
  const letters = initials(account.name);
  document.querySelector('#accountAvatar').textContent = letters;
  document.querySelector('#profileAvatar').textContent = letters;
  document.querySelector('#accountName').textContent = account.name;
  document.querySelector('#profileName').textContent = account.name;
  document.querySelector('#accountEmail').textContent = account.email;
  document.querySelector('#profileEmail').textContent = account.email;
  const folder = state.folders.find(item => item.id === state.folderId);
  document.querySelector('.eyebrow span').textContent = folder?.name || account.name;
  document.querySelector('#welcomeTitle').textContent = folder ? `Обзор папки «${folder.name}»` : 'Обзор ваших проектов';
  document.querySelector('.admin-nav').hidden = account.role !== 'admin';
}

function showAuth(register = false) {
  state.authenticated = false;
  document.body.classList.remove('authenticated');
  document.body.classList.remove('admin-page');
  const title = document.querySelector('#authTitle');
  const description = document.querySelector('#authDescription');
  const nameField = document.querySelector('#authNameField');
  const submit = document.querySelector('.auth-submit');
  title.textContent = register ? 'Создайте личный кабинет' : 'Войдите в кабинет';
  description.textContent = register ? 'В вашем кабинете уже будет первая папка с VK, Telegram и MAX.' : 'Введите почту и пароль или зарегистрируйтесь.';
  nameField.hidden = !register;
  nameField.querySelector('input').required = register;
  document.querySelector('#authForm [name="password"]').autocomplete = register ? 'new-password' : 'current-password';
  submit.textContent = register ? 'Создать кабинет' : 'Войти';
  document.querySelector('#authSwitch').textContent = register ? 'Уже есть аккаунт? Войти' : 'Нет аккаунта? Зарегистрироваться';
  document.querySelector('#authForm').dataset.mode = register ? 'register' : 'login';
  document.querySelector('#authError').textContent = '';
}

function openAuth(register) {
  showAuth(register);
  const dialog = document.querySelector('#authDialog');
  if (!dialog.open) dialog.showModal();
  dialog.querySelector(register ? '[name="name"]' : '[name="email"]').focus();
}

async function bootstrap() {
  try {
    const status = await api('/api/auth/status');
    if (!status.authenticated) {
      showAuth(false);
      return;
    }
    state.authenticated = true;
    document.body.classList.add('authenticated');
    document.querySelector('#authDialog').close();
    applyAccount(status.account);
    await loadFolders();
    const inviteToken = new URLSearchParams(location.search).get('invite');
    if (inviteToken) {
      try { await api('/api/invitations/accept', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token: inviteToken }) }); history.replaceState({}, '', location.pathname); await loadFolders(); showToast('Доступ принят', 'Папка появилась в разделе «Доступные мне».'); }
      catch (error) { showToast('Не удалось принять приглашение', error.message, true); }
    }
    if (status.account.role === 'admin') navigate('admin');
    else navigate('overview');
  } catch (error) {
    showAuth(false);
    document.querySelector('#authError').textContent = `Сервер недоступен: ${error.message}`;
  }
}

function folderQuery(path) {
  return `${path}${path.includes('?') ? '&' : '?'}folder_id=${encodeURIComponent(state.folderId)}`;
}

async function loadFolders(preferred) {
  const [data, status] = await Promise.all([api('/api/folders'), api('/api/auth/status')]);
  if (status.account) applyAccount(status.account);
  state.ownedFolders = data.folders;
  state.sharedFolders = data.shared_folders || [];
  state.folders = [...state.ownedFolders, ...state.sharedFolders];
  state.folderLimit = data.limit;
  state.folderId = state.folders.find(f => f.id === (preferred || state.folderId) && !f.blocked)?.id || state.folders.find(f => !f.blocked)?.id || null;
  applyAccount(state.account);
  const select = document.querySelector('#folderSelect');
  select.innerHTML = state.folders.map(f => `<option value="${escapeHtml(f.id)}" ${f.blocked ? 'disabled' : ''}>${escapeHtml(f.name)}${f.role !== 'owner' ? ` · ${roleLabel(f.role)}` : ''}${f.blocked ? ' (заблокирована)' : ''}</option>`).join('');
  if (state.folderId) select.value = state.folderId;
  select.disabled = !state.folderId;
  const selectedFolder = state.folders.find(f => f.id === state.folderId);
  document.querySelector('#renameFolder').disabled = !selectedFolder || selectedFolder.role !== 'owner';
  document.querySelector('#folderLimit').textContent = `${data.folders.length} из ${data.limit}`;
  renderFolderCards();
  const canCreate = data.folders.length < data.limit;
  document.querySelector('#createFolder').hidden = !canCreate;
  document.querySelector('#requestFolder').hidden = canCreate;
  document.querySelector('#folderFootnote').hidden = canCreate;
  document.querySelector('#premiumBadge').hidden = !state.account?.premium;
  document.querySelector('#emptyWorkspace').hidden = Boolean(state.folderId) || document.body.classList.contains('admin-page');
  document.querySelectorAll('.page').forEach(page => { if (page.id !== 'page-admin') page.classList.toggle('workspace-hidden', !state.folderId); });
  document.querySelector('#syncButton').disabled = !state.folderId;
  if (state.folderId) await Promise.all([loadDashboard(), renderConnections(), loadCabinet()]);
  else { state.dashboard = null; document.querySelector('#connectionGrid').innerHTML = ''; }
}

function renderFolderCards() {
  const target = document.querySelector('#folderCards');
  const card = folder => `<article class="folder-card ${folder.id === state.folderId ? 'selected' : ''}"><span class="folder-card-icon" data-icon="layers"></span><div><strong>${escapeHtml(folder.name)}</strong><p>${folder.blocked ? 'Доступ к папке ограничен' : folder.role === 'owner' ? 'ВКонтакте · Telegram · MAX' : `Владелец: ${escapeHtml(folder.owner_name || folder.owner_email)} · ${roleLabel(folder.role)}`}</p></div><div class="folder-card-actions"><button class="outline-button" data-open-folder="${escapeHtml(folder.id)}" ${folder.blocked ? 'disabled' : ''}>${folder.id === state.folderId ? 'Открыта' : 'Открыть папку'} →</button>${folder.role === 'owner' ? `<button class="outline-button" data-rename-folder="${escapeHtml(folder.id)}" ${folder.blocked ? 'disabled' : ''}>Переименовать</button>` : ''}</div></article>`;
  target.innerHTML = state.ownedFolders.map(card).join('');
  const shared = document.querySelector('#sharedFolderCards');
  shared.innerHTML = state.sharedFolders.map(card).join('') || '<p class="history-empty">Пока нет приглашений в папки.</p>';
  const bind = root => {
    root.querySelectorAll('[data-open-folder]').forEach(button => button.addEventListener('click', async () => { await loadFolders(button.dataset.openFolder); navigate('overview'); }));
    root.querySelectorAll('[data-rename-folder]').forEach(button => button.addEventListener('click', () => renameFolder(button.dataset.renameFolder)));
  };
  hydrateIcons(target);
  hydrateIcons(shared); bind(target); bind(shared);
}

function roleLabel(role) { return ({ owner: 'Владелец', editor: 'Редактор', viewer: 'Наблюдатель' }[role] || role || 'Участник'); }

async function renameFolder(folderId) {
  const folder = state.folders.find(item => item.id === folderId && !item.blocked);
  if (!folder) return;
  const answer = window.prompt('Новое название папки', folder.name);
  if (answer === null || answer.trim() === folder.name) return;
  const name = answer.trim();
  if (!name || name.length > 100) {
    showToast('Не удалось переименовать папку', 'Название должно содержать от 1 до 100 символов.', true);
    return;
  }
  try {
    await api('/api/folders/rename', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ folder_id: folderId, name }) });
    await loadFolders(state.folderId);
    showToast('Папка переименована', `Новое название: ${name}`);
  } catch (error) { showToast('Не удалось переименовать папку', error.message, true); }
}

async function createFolder() {
  const name = window.prompt('Название новой папки');
  if (name === null) return;
  try {
    const data = await api('/api/folders/create', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name }) });
    await loadFolders(data.folder.id);
    navigate('connections');
    showToast('Папка создана', 'Теперь подключите свои проекты VK, Telegram и MAX.');
  } catch (error) { showToast('Не удалось создать папку', error.message, true); }
}

async function renderAdmin() {
  if (state.account?.role !== 'admin') return;
  const data = await api('/api/admin');
  document.querySelector('#adminUsers').innerHTML = data.users.map(user => {
    const own = user.id === state.account.id;
    return `<article class="card admin-user"><div class="admin-head"><div><h3>${escapeHtml(user.name)}</h3><p>${escapeHtml(user.email)} · ${user.role === 'admin' ? 'Администратор' : 'Пользователь'} · ${user.premium ? 'Премиум' : 'Базовый'}</p></div>${own ? '' : `<div class="admin-actions"><button class="outline-button" data-admin="premium" data-user="${user.id}" data-value="${!user.premium}">${user.premium ? 'Забрать премиум' : 'Выдать премиум'}</button><button class="outline-button danger-button" data-admin="blocked" data-user="${user.id}" data-value="${!user.blocked}">${user.blocked ? 'Разблокировать' : 'Заблокировать'}</button></div>`}</div>${own ? '' : `<label class="admin-quota">Дополнительные папки <input type="number" min="0" max="100" value="${user.extra_folders || 0}" data-quota="${user.id}"></label>`}<span class="admin-caption">${user.folders.length} папок создано</span><div class="admin-folders">${user.folders.map(folder => `<div class="admin-folder"><div><strong>${escapeHtml(folder.name)}</strong>${own ? '' : `<button class="outline-button" data-admin="folder_blocked" data-user="${user.id}" data-folder="${folder.id}" data-value="${!folder.blocked}">${folder.blocked ? 'Разблокировать папку' : 'Блокировать папку'}</button>`}</div>${folder.projects.length ? folder.projects.map(project => `<div class="admin-project"><span>${escapeHtml(platformLabels[project.platform])} · ${escapeHtml(project.url)}</span>${own ? '' : `<button class="outline-button" data-admin="project_blocked" data-user="${user.id}" data-folder="${folder.id}" data-platform="${project.platform}" data-value="${!project.blocked}">${project.blocked ? 'Разблокировать' : 'Блокировать'}</button>`}</div>`).join('') : '<p>Проектов пока нет</p>'}</div>`).join('') || '<p>Папок пока нет</p>'}</div></article>`;
  }).join('');
  document.querySelectorAll('[data-admin]').forEach(button => button.addEventListener('click', async () => {
    await adminUpdate({ field: button.dataset.admin, user_id: button.dataset.user, folder_id: button.dataset.folder, platform: button.dataset.platform, value: button.dataset.value === 'true' });
  }));
  document.querySelectorAll('[data-quota]').forEach(input => input.addEventListener('change', async () => adminUpdate({ field: 'extra_folders', user_id: input.dataset.quota, value: Number(input.value) })));
}

async function adminUpdate(payload) {
  try {
    await api('/api/admin/update', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    await renderAdmin();
    await loadFolders();
    showToast('Изменения сохранены', 'Права доступа обновлены.');
  } catch (error) { showToast('Ошибка', error.message, true); await renderAdmin(); }
}

async function loadCabinet() {
  const cabinet = await api(folderQuery('/api/cabinet'));
  state.cabinet = cabinet;
  applyAccount(cabinet.account);
  const banner = document.querySelector('#realtimeBanner');
  banner.className = `realtime-banner${cabinet.realtime_available ? ' ready' : ''}`;
  banner.innerHTML = `<span class="banner-icon">${icon(cabinet.realtime_available ? 'check' : 'alert')}</span><div><strong>${cabinet.realtime_available ? 'Режим реального времени доступен' : 'Сейчас работает периодический сбор'}</strong>${cabinet.realtime_available ? `Webhook-адреса сформированы для ${escapeHtml(cabinet.public_base_url)}.` : 'Для мгновенных событий нужен публичный HTTPS-адрес. Укажите PUBLIC_BASE_URL на сервере; localhost недоступен социальным сетям.'}</div>`;
  const folder = state.folders.find(item => item.id === state.folderId);
  const viewer = folder?.role === 'viewer';
  document.querySelector('#syncAll').hidden = viewer;
  document.querySelector('#connectionSettings').hidden = viewer;
  document.querySelectorAll('[data-connect]').forEach(button => { button.hidden = viewer; });
  const accessCard = document.querySelector('#accessCard');
  accessCard.hidden = folder?.role !== 'owner';
  if (folder?.role === 'owner') await renderAccess();
  return cabinet;
}

async function renderAccess() {
  const data = await api(folderQuery('/api/folder/access'));
  const target = document.querySelector('#accessMembers');
  const members = data.members.map(member => `<div class="access-row"><div><strong>${escapeHtml(member.name || member.email)}</strong><small>${escapeHtml(member.email)}</small></div><select data-member-role="${member.id}"><option value="editor" ${member.role === 'editor' ? 'selected' : ''}>Редактор</option><option value="viewer" ${member.role === 'viewer' ? 'selected' : ''}>Наблюдатель</option></select><button class="text-button danger-text" data-remove-member="${member.id}">Удалить</button></div>`).join('');
  const invites = data.invites.map(invite => `<div class="access-row invite-row"><div><strong>Одноразовая ссылка</strong><small>Действует до ${new Date(invite.expires_at).toLocaleDateString('ru-RU')} · Редактор</small></div><button class="text-button danger-text" data-cancel-invite="${invite.id}">Отменить</button></div>`).join('');
  target.innerHTML = members + invites || '<p class="history-empty">Участников пока нет.</p>';
  target.querySelectorAll('[data-member-role]').forEach(select => select.addEventListener('change', async () => { await api('/api/folders/member-update', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ folder_id: state.folderId, member_id: select.dataset.memberRole, role: select.value }) }); showToast('Роль изменена', 'Новые права применены сразу.'); }));
  target.querySelectorAll('[data-remove-member]').forEach(button => button.addEventListener('click', async () => { if (!confirm('Удалить участника из папки?')) return; await api('/api/folders/member-remove', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ folder_id: state.folderId, member_id: button.dataset.removeMember }) }); await renderAccess(); showToast('Доступ отозван', 'Участник больше не видит эту папку.'); }));
  target.querySelectorAll('[data-cancel-invite]').forEach(button => button.addEventListener('click', async () => { await api('/api/folders/invite-cancel', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ folder_id: state.folderId, invite_id: button.dataset.cancelInvite }) }); await renderAccess(); }));
  document.querySelector('#inviteMember').onclick = async () => {
    try {
      const result = await api('/api/folders/invite', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ folder_id: state.folderId }) });
      try { await navigator.clipboard.writeText(result.invite.url); } catch (_) {}
      prompt('Одноразовая ссылка скопирована. Передайте её сотруднику. После принятия она станет недействительной:', result.invite.url);
      await renderAccess();
    } catch (error) { showToast('Не удалось создать приглашение', error.message, true); }
  };
}

async function loadDashboard() {
  try {
    const data = await api(folderQuery(`/api/dashboard?period=${state.period}`));
    state.dashboard = data;
    renderDashboard();
  } catch (error) {
    showToast('Не удалось загрузить данные', error.message, true);
  }
}

function renderDashboard() {
  const data = state.dashboard;
  if (!data) return;
  renderKpis(data.summary);
  renderChart();
  renderAudience(data.audience);
  renderPlatforms(data.platforms);
  renderPosts(data.posts.slice(0, 4), document.querySelector('#topPosts'), false);
  renderInsights(data.insights);
  renderContent();
  if (document.querySelector('#page-reports').classList.contains('active')) loadHistoryReports();
  updateSyncText(data.last_sync);
  document.querySelector('#contentCount').textContent = data.posts.length;
}

function renderKpis(items) {
  const themes = [
    { icon: 'users', color: '#315bff', tint: '#eaf0ff' },
    { icon: 'eye', color: '#2787f5', tint: '#eaf3ff' },
    { icon: 'heart', color: '#e66589', tint: '#fff0f4' },
    { icon: 'layers', color: '#f09b47', tint: '#fff5e9' },
  ];
  document.querySelector('#kpiGrid').innerHTML = items.map((item, index) => {
    const theme = themes[index];
    const change = Number(item.change) || 0;
    return `<article class="kpi-card" style="--card-color:${theme.color};--card-tint:${theme.tint}">
      <div class="kpi-top"><span class="kpi-icon">${icon(theme.icon)}</span><span class="kpi-change${change === 0 ? ' neutral' : ''}">${change === 0 ? '—' : icon('arrowUp') + ' ' + escapeHtml(String(change).replace('.', ',')) + '%'}</span></div>
      <strong class="kpi-value">${formatKpi(item)}</strong>
      <div class="kpi-bottom"><span class="kpi-label">${escapeHtml(item.label)}</span><span class="kpi-caption">${escapeHtml(item.caption)}</span></div>
    </article>`;
  }).join('');
}

function renderChart() {
  const container = document.querySelector('#trendChart');
  const data = state.dashboard.trend;
  const metric = state.metric;
  const values = data.map(point => point[metric]);
  const width = 740, height = 218, left = 43, right = 10, top = 16, bottom = 29;
  const innerW = width - left - right, innerH = height - top - bottom;
  let min = Math.min(...values), max = Math.max(...values);
  const pad = Math.max((max - min) * .18, metric === 'engagement' ? .3 : 100);
  min -= pad; max += pad;
  const x = index => left + (index / Math.max(values.length - 1, 1)) * innerW;
  const y = value => top + (1 - ((value - min) / Math.max(max - min, 1))) * innerH;
  const points = values.map((value, i) => `${x(i).toFixed(1)},${y(value).toFixed(1)}`).join(' ');
  const linePath = values.map((value, i) => `${i ? 'L' : 'M'}${x(i).toFixed(1)} ${y(value).toFixed(1)}`).join(' ');
  const areaPath = `${linePath} L${x(values.length - 1)} ${top + innerH} L${x(0)} ${top + innerH} Z`;
  const yTicks = Array.from({ length: 5 }, (_, i) => max - ((max - min) / 4) * i);
  const labelEvery = Math.max(1, Math.ceil(data.length / 6));
  const formatAxis = value => metric === 'engagement' ? `${value.toFixed(1).replace('.', ',')}%` : formatCompact(value);

  container.innerHTML = `<svg class="trend-svg" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" aria-label="График динамики ${metric}">
    <defs><linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#315bff" stop-opacity=".20"/><stop offset="100%" stop-color="#315bff" stop-opacity="0"/></linearGradient></defs>
    ${yTicks.map((tick, i) => `<line class="grid-line" x1="${left}" x2="${width - right}" y1="${top + (innerH / 4) * i}" y2="${top + (innerH / 4) * i}"/><text class="axis-label" x="0" y="${top + (innerH / 4) * i + 3}">${formatAxis(tick)}</text>`).join('')}
    ${data.map((point, i) => (i % labelEvery === 0 || i === data.length - 1) ? `<text class="axis-label" text-anchor="middle" x="${x(i)}" y="${height - 4}">${point.date}</text>` : '').join('')}
    <path class="trend-area" d="${areaPath}"/><path class="trend-line" d="${linePath}"/>
    <line class="hover-line" id="hoverLine" y1="${top}" y2="${top + innerH}"/>
    ${data.map((point, i) => `<circle class="trend-point" data-point="${i}" cx="${x(i)}" cy="${y(values[i])}" r="4"/>`).join('')}
    ${data.map((point, i) => `<rect class="chart-hit" data-hit="${i}" x="${i === 0 ? left : (x(i - 1) + x(i)) / 2}" y="${top}" width="${i === data.length - 1 ? width - right - x(i) : (x(i + 1) - x(i - 1)) / 2}" height="${innerH}"/>`).join('')}
  </svg><div class="chart-tooltip" id="chartTooltip"></div>`;

  const tooltip = container.querySelector('#chartTooltip');
  const hoverLine = container.querySelector('#hoverLine');
  container.querySelectorAll('[data-hit]').forEach(hit => {
    hit.addEventListener('mouseenter', () => showChartPoint(Number(hit.dataset.hit)));
    hit.addEventListener('mousemove', () => showChartPoint(Number(hit.dataset.hit)));
  });
  container.addEventListener('mouseleave', () => {
    tooltip.style.opacity = '0';
    hoverLine.style.opacity = '0';
    container.querySelectorAll('.trend-point').forEach(point => point.style.opacity = '0');
  });

  function showChartPoint(index) {
    const point = data[index];
    const cx = x(index), cy = y(values[index]);
    container.querySelectorAll('.trend-point').forEach((node, i) => node.style.opacity = i === index ? '1' : '0');
    hoverLine.setAttribute('x1', cx); hoverLine.setAttribute('x2', cx); hoverLine.style.opacity = '1';
    const label = metric === 'engagement' ? `${String(point[metric]).replace('.', ',')}%` : formatNumber(point[metric]);
    tooltip.innerHTML = `<span>${escapeHtml(point.date)}</span><strong>${label}</strong>`;
    tooltip.style.left = `${(cx / width) * 100}%`;
    tooltip.style.top = `${(cy / height) * 100}%`;
    tooltip.style.opacity = '1';
  }

  const labels = { audience: 'Общая аудитория', reach: 'Суммарный охват', engagement: 'Вовлечённость' };
  document.querySelector('#chartLegend').innerHTML = `<span><i></i>${labels[metric]}</span><span><i style="background:#dcd8f8"></i>Предыдущий период</span>`;
}

function renderAudience(audience) {
  const netLabel = audience.net > 0 ? `+${formatNumber(audience.net)}` : audience.net < 0 ? `−${formatNumber(Math.abs(audience.net))}` : '—';
  const conversion = audience.new ? `${(audience.net / audience.new * 100).toFixed(1).replace('.', ',')}%` : '—';
  document.querySelector('#audienceDonut').innerHTML = `<div><strong>${netLabel}</strong><span>${audience.net ? 'чистый прирост' : 'копим историю'}</span></div>`;
  document.querySelector('#audienceStats').innerHTML = `
    <div><span>Подписались</span><strong>+${formatNumber(audience.new)}</strong></div>
    <div><span>Отписались</span><strong>−${formatNumber(audience.left)}</strong></div>
    <div><span>Конверсия</span><strong>${conversion}</strong></div>`;
  const note = document.querySelector('.mini-note p');
  if (audience.net) {
    note.innerHTML = `<strong>${audience.net > 0 ? 'Аудитория растёт' : 'Есть снижение'}</strong>: ${netLabel} за выбранный период`;
  } else {
    note.innerHTML = '<strong>История накапливается</strong>: динамика появится после следующих замеров';
  }
}

function sparkline(platform) {
  const values = platform.history?.length > 1 ? platform.history : [platform.subscribers, platform.subscribers];
  const min = Math.min(...values), max = Math.max(...values);
  const span = Math.max(max - min, 1);
  const points = values.map((value, i) => `${(i / Math.max(values.length - 1, 1) * 90).toFixed(1)},${(28 - ((value - min) / span) * 22).toFixed(1)}`).join(' ');
  return `<svg class="sparkline" viewBox="0 0 92 34"><path class="area" d="M${points.split(' ').join(' L')} L90 34 L0 34Z"/><path class="line" d="M${points.split(' ').join(' L')}"/></svg>`;
}

function renderPlatforms(platforms) {
  document.querySelector('#platformGrid').innerHTML = platforms.map(item => `<article class="platform-card" style="--platform-color:${item.color}">
    <div class="platform-card-head"><span class="platform-icon ${item.id}">${platformLetters[item.id]}</span><div><strong>${escapeHtml(item.name)}</strong><small>${escapeHtml(item.handle)}</small></div><span class="platform-badge ${item.status === 'connected' ? '' : 'demo'}">${item.status === 'connected' ? 'Собирается' : 'Ожидание'}</span></div>
    <div class="platform-main"><div><span>Подписчики</span><strong>${formatNumber(item.subscribers)}</strong><div class="platform-growth">${item.growth ? icon('arrowUp') + ' ' + String(item.growth).replace('.', ',') + '%' : 'история копится'}</div></div>${sparkline(item)}</div>
    <div class="platform-metrics"><div><span>Охват</span><strong>${formatCompact(item.reach)}</strong></div><div><span>ER</span><strong>${String(item.engagement).replace('.', ',')}%</strong></div><div><span>Посты</span><strong>${item.posts}</strong></div></div>
  </article>`).join('');
}

function postRow(post, full) {
  const title = post.url ? `<a href="${escapeHtml(post.url)}" target="_blank" rel="noopener">${escapeHtml(post.title)}</a>` : escapeHtml(post.title);
  return `<tr>
    <td><div class="post-cell"><span class="post-platform ${post.platform}">${platformLetters[post.platform]}</span><div class="post-copy"><strong title="${escapeHtml(post.title)}">${title}</strong><span>${escapeHtml(platformLabels[post.platform])} · ${escapeHtml(post.date)}</span></div></div></td>
    ${full ? `<td><span class="type-badge">${escapeHtml(post.type)}</span></td>` : ''}
    <td>${formatNumber(post.reach)}</td><td>${formatNumber(post.reactions)}</td>
    ${full ? `<td>${formatNumber(post.comments)}</td>` : ''}
    <td><span class="er-badge">${String(post.er).replace('.', ',')}%</span></td>
    ${full ? `<td class="${post.trend >= 0 ? 'trend-up' : 'trend-down'}">${post.trend >= 0 ? '+' : ''}${post.trend}%</td>` : ''}
  </tr>`;
}

function renderPosts(posts, target, full) {
  target.innerHTML = posts.length ? posts.map(post => postRow(post, full)).join('') : `<tr><td colspan="7" class="empty-row">Ничего не найдено. Измените фильтр или запрос.</td></tr>`;
}

function renderInsights(items) {
  const symbols = ['chart', 'clock', 'target'];
  const colors = { violet: ['#315bff', '#eaf0ff'], green: ['#1dac74', '#e9f8f1'], blue: ['#2787f5', '#eaf3ff'] };
  document.querySelector('#insightList').innerHTML = items.map((item, index) => `<div class="insight-item" style="--tone:${colors[item.tone][0]};--tone-bg:${colors[item.tone][1]}"><span class="insight-symbol">${icon(symbols[index])}</span><div><strong>${escapeHtml(item.title)}</strong><p>${escapeHtml(item.text)}</p></div></div>`).join('');
}

function renderContent() {
  if (!state.dashboard) return;
  const query = state.search.toLocaleLowerCase('ru');
  const posts = state.dashboard.posts
    .filter(post => state.contentPlatform === 'all' || post.platform === state.contentPlatform)
    .filter(post => !query || post.title.toLocaleLowerCase('ru').includes(query) || post.type.toLocaleLowerCase('ru').includes(query))
    .sort((a, b) => state.sortDesc ? b.er - a.er : a.er - b.er);
  renderPosts(posts, document.querySelector('#allPosts'), true);
  document.querySelector('#sortErMobile').textContent = `ER ${state.sortDesc ? '↓' : '↑'}`;
  document.querySelector('#contentMobile').innerHTML = posts.length ? posts.map(post => `<article class="content-mobile-card"><div class="content-mobile-head"><span class="post-platform ${post.platform}">${platformLetters[post.platform]}</span><div><strong>${post.url ? `<a href="${escapeHtml(post.url)}" target="_blank" rel="noopener">${escapeHtml(post.title)}</a>` : escapeHtml(post.title)}</strong><small>${escapeHtml(platformLabels[post.platform])} · ${escapeHtml(post.date)}</small></div></div><div class="content-mobile-metrics"><span>Просмотры <strong>${formatNumber(post.reach)}</strong></span><span>Реакции <strong>${formatNumber(post.reactions)}</strong></span><span>Комментарии <strong>${formatNumber(post.comments)}</strong></span><span>ER <strong>${escapeHtml(String(post.er).replace('.', ','))}%</strong></span></div></article>`).join('') : '<p class="history-empty">Публикаций пока нет.</p>';
}

const monthLabels = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];

function historyTable(data) {
  if (!data.platforms.length) return '<p class="history-empty">Подключите хотя бы одну площадку в этой папке.</p>';
  const numberOrDash = value => value === null ? '—' : formatNumber(value);
  const current = new Date();
  const future = row => data.year === current.getUTCFullYear() && (data.grouping === 'month' ? row.period > current.getUTCMonth() + 1 : row.period > Math.floor(current.getUTCMonth() / 3) + 1);
  const available = data.rows.filter(row => row.observed_days || row.posts !== null || row.vk_reach !== null).length;
  return `<p class="history-note">Аудитория — последний сохранённый замер периода; изменение — между первым и последним днями с замером. Просмотры и реакции — только по зафиксированным публикациям. Охват VK — отдельная метрика официального API, не сумма просмотров. Отсутствие данных не означает ноль.</p>
    ${!available ? '<p class="history-empty">За выбранный год пока нет сохранённых данных. Для VK можно запросить архив через API, если подключён токен администратора.</p>' : ''}
    <div class="table-wrap history-desktop"><table class="history-table"><thead><tr><th>Период</th><th>Площадка</th><th>Аудитория</th><th>Изменение</th><th>Публикации</th><th>Просмотры</th><th>Реакции</th><th>Охват VK</th></tr></thead><tbody>${data.rows.map(row => `<tr class="${!row.observed_days && row.posts === null && row.vk_reach === null ? 'history-no-data' : ''}"><td>${data.grouping === 'month' ? monthLabels[row.period - 1] : `${row.period} квартал`}</td><td>${escapeHtml(platformLabels[row.platform])}</td><td>${numberOrDash(row.audience)}</td><td>${row.audience_change === null ? '—' : `${row.audience_change > 0 ? '+' : ''}${formatNumber(row.audience_change)}`}</td><td>${numberOrDash(row.posts)}</td><td>${numberOrDash(row.post_views)}</td><td>${numberOrDash(row.reactions)}</td><td>${numberOrDash(row.vk_reach)}</td></tr>`).join('')}</tbody></table></div>
    <div class="history-mobile">${Array.from({ length: data.grouping === 'month' ? 12 : 4 }, (_, i) => `<article class="history-period"><h4>${data.grouping === 'month' ? monthLabels[i] : `${i + 1} квартал`}</h4>${data.rows.filter(row => row.period === i + 1).map(row => `<div class="history-period-network"><strong>${escapeHtml(platformLabels[row.platform])}</strong>${row.audience === null && row.posts === null && row.vk_reach === null ? `<span class="history-period-empty">${future(row) ? 'Период ещё не наступил' : 'Нет данных'}</span>` : `<dl><div><dt>Аудитория</dt><dd>${numberOrDash(row.audience)}</dd></div><div><dt>Изменение</dt><dd>${numberOrDash(row.audience_change)}</dd></div><div><dt>Публикации</dt><dd>${numberOrDash(row.posts)}</dd></div><div><dt>Просмотры</dt><dd>${numberOrDash(row.post_views)}</dd></div><div><dt>Реакции</dt><dd>${numberOrDash(row.reactions)}</dd></div>${row.platform === 'vk' ? `<div><dt>Охват VK</dt><dd>${numberOrDash(row.vk_reach)}</dd></div>` : ''}</dl>`}</div>`).join('')}</article>`).join('')}</div><p class="history-footnote">${available} из ${data.rows.length} строк содержат данные. ${data.vk_fetched_at ? `Архив VK загружен ${escapeHtml(new Date(data.vk_fetched_at).toLocaleDateString('ru-RU'))}.` : ''}</p>`;
}

async function loadHistorySection(kind) {
  if (!state.folderId) return;
  const folderId = state.folderId;
  const current = kind === 'current';
  const year = current ? new Date().getUTCFullYear() : state.archiveYear;
  const grouping = document.querySelector(current ? '#currentGrouping' : '#archiveGrouping').value;
  const target = document.querySelector(current ? '#currentHistory' : '#archiveHistory');
  target.innerHTML = '<p class="history-empty">Загружаем историю…</p>';
  try {
    const data = await api(folderQuery(`/api/history/report?year=${year}&grouping=${grouping}`));
    if (state.folderId !== folderId || (!current && state.archiveYear !== year)) return;
    target.innerHTML = historyTable(data);
    document.querySelector(current ? '#currentVkBackfill' : '#archiveVkBackfill').hidden = !data.vk_available;
  } catch (error) { target.innerHTML = `<p class="history-empty">${escapeHtml(error.message)}</p>`; }
}

async function loadHistoryReports() {
  if (!state.folderId) return;
  document.querySelector('#currentYearTitle').textContent = `Текущий год · ${new Date().getUTCFullYear()}`;
  const select = document.querySelector('#archiveYear');
  if (!select.options.length) {
    for (let year = new Date().getUTCFullYear() - 1; year >= 2006; year--) select.add(new Option(String(year), String(year)));
  }
  select.value = String(state.archiveYear);
  await Promise.all([loadHistorySection('current'), loadHistorySection('archive')]);
}

async function backfillVk(kind) {
  const current = kind === 'current';
  const year = current ? new Date().getUTCFullYear() : state.archiveYear;
  const button = document.querySelector(current ? '#currentVkBackfill' : '#archiveVkBackfill');
  button.disabled = true;
  button.textContent = 'Загружаем…';
  try {
    const result = await api('/api/history/backfill', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ folder_id: state.folderId, year }) });
    await loadHistorySection(kind);
    showToast('История VK обновлена', result.months_available ? `Получено месяцев: ${result.months_available}.` : 'VK не предоставил данные за выбранный год.');
  } catch (error) { showToast('Не удалось получить историю VK', error.message, true); }
  finally { button.disabled = false; button.textContent = 'Загрузить историю VK'; }
}

async function renderConnections() {
  const target = document.querySelector('#connectionGrid');
  try {
    const { connections } = await api(folderQuery('/api/connections'));
    target.innerHTML = connections.map(item => {
      const status = item.status === 'connected' ? 'Подключено' : item.status === 'error' ? 'Ошибка' : 'Готово к проверке';
      const time = item.last_sync ? new Date(item.last_sync).toLocaleString('ru-RU', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : 'ещё не было';
      const method = item.source === 'api' ? 'Официальный API' : 'Публичная страница';
      return `<article class="connection-card"><div class="connection-head"><span class="platform-icon ${item.id}">${platformLetters[item.id]}</span><div><strong>${escapeHtml(item.name)}</strong><small>${platformLabels[item.id]}</small></div><span class="connection-state ${item.status === 'connected' ? '' : item.status === 'error' ? 'error' : 'demo'}"><i></i>${status}</span></div><div class="connection-info"><div><span>Источник</span><strong>${method}</strong></div><div><span>Последняя проверка</span><strong>${time}</strong></div><div><span>Адрес</span><strong>${escapeHtml((item.url || '').replace(/^https?:\/\//, '')) || 'Не указан'}</strong></div></div><div class="connection-flags"><span class="connection-flag ${item.has_token ? 'on' : ''}">${item.has_token ? 'API подключён' : 'Только публично'}</span><span class="connection-flag ${item.realtime ? 'on' : ''}">${item.realtime ? 'Webhook активен' : 'Без realtime'}</span></div>${item.error ? `<p class="connection-error">${escapeHtml(item.error)}</p>` : ''}<div class="connection-actions">${item.url ? `<a class="outline-button" href="${escapeHtml(item.url)}" target="_blank" rel="noopener">Открыть страницу</a>` : ''}<button class="outline-button" data-connect="${item.id}">${item.has_token ? 'Изменить доступ' : 'Подключить проект'}</button></div></article>`;
    }).join('');
    target.querySelectorAll('[data-connect]').forEach(button => button.addEventListener('click', () => showConnectionHelp(button.dataset.connect)));
    document.querySelectorAll('.platform-nav .status-dot').forEach((dot, index) => {
      dot.classList.toggle('demo', connections.find(c => c.id === ['vk', 'telegram', 'max'][index])?.status !== 'connected');
    });
  } catch (error) {
    target.innerHTML = `<article class="connection-card"><p class="connection-error">${escapeHtml(error.message)}</p></article>`;
  }
}

function navigate(page) {
  document.body.classList.toggle('admin-page', page === 'admin');
  document.querySelector('#emptyWorkspace').hidden = Boolean(state.folderId) || page === 'admin';
  document.querySelectorAll('.page').forEach(node => node.classList.toggle('active', node.id === `page-${page}`));
  document.querySelectorAll('.nav-item').forEach(node => node.classList.toggle('active', node.dataset.page === page));
  const titles = { overview: 'Обзор', content: 'Контент', reports: 'Отчёты', connections: 'Личный кабинет', admin: 'Администратор' };
  document.querySelector('#pageTitle').textContent = titles[page];
  if (page === 'connections' && state.folderId) Promise.all([renderConnections(), loadCabinet()]);
  if (page === 'admin') renderAdmin();
  if (page === 'reports' && state.folderId) loadHistoryReports();
  closeMobileMenu();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function syncAll(trigger) {
  const buttons = [document.querySelector('#syncButton'), document.querySelector('#syncAll')].filter(Boolean);
  buttons.forEach(button => { button.classList.add('loading'); button.disabled = true; });
  try {
    const result = await api('/api/sync', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ folder_id: state.folderId }) });
    const live = result.connections.filter(connection => connection.status === 'connected').length;
    const errors = result.connections.filter(connection => connection.status === 'error').length;
    await loadDashboard();
    await renderConnections();
    showToast('Синхронизация завершена', live ? `Источников обновлено: ${live}${errors ? `, с ошибкой: ${errors}` : ''}.` : 'Не удалось обновить источники.', Boolean(errors));
  } catch (error) {
    showToast('Ошибка синхронизации', error.message, true);
  } finally {
    buttons.forEach(button => { button.classList.remove('loading'); button.disabled = false; });
  }
}

function updateSyncText(timestamp) {
  const target = document.querySelector('#updatedText');
  if (!timestamp) { target.textContent = 'Синхронизация ещё не запускалась'; return; }
  const date = new Date(timestamp);
  target.textContent = `Обновлено ${date.toLocaleString('ru-RU', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })}`;
}

function showToast(title, message, isError = false) {
  const toast = document.createElement('div');
  toast.className = `toast${isError ? ' error' : ''}`;
  toast.innerHTML = `<span class="toast-icon">${icon(isError ? 'alert' : 'check')}</span><div><strong>${escapeHtml(title)}</strong><span>${escapeHtml(message)}</span></div>`;
  document.querySelector('#toastRegion').appendChild(toast);
  window.setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateY(8px)'; }, 3800);
  window.setTimeout(() => toast.remove(), 4100);
}

function openModal(title, content) {
  document.querySelector('#modalTitle').textContent = title;
  document.querySelector('#modalContent').innerHTML = content;
  const modal = document.querySelector('#infoModal');
  if (!modal.open) modal.showModal();
}

function setupContent() {
  return `<p>В первой папке доступны три площадки: VK, Telegram и MAX. В разделе <strong>Личный кабинет</strong> укажите свои ссылки и подключите нужные проекты.</p><ol><li><strong>Ссылка канала</strong> включает публичный сбор.</li><li><strong>Токен API</strong> даёт доступ к административным метрикам.</li><li><strong>Webhook</strong> присылает новые события сразу после появления.</li></ol><p>Если понадобится ещё одна папка, нажмите «Добавить папку» над кабинетом.</p>`;
}

function copyBox(value, label) {
  if (!value) return `<div class="copy-field"><code>${escapeHtml(label)}</code><button type="button" disabled>Нет адреса</button></div>`;
  return `<div class="copy-field"><code title="${escapeHtml(value)}">${escapeHtml(value)}</code><button type="button" data-copy="${escapeHtml(value)}">Копировать</button></div>`;
}

function connectionGuide(platform, config, realtimeAvailable) {
  const webhook = config.webhook_url;
  const secret = config.webhook_secret;
  const realtimeNotice = `<div class="guide-notice ${realtimeAvailable ? 'ready' : ''}">${icon(realtimeAvailable ? 'check' : 'alert')}<span>${realtimeAvailable ? 'Публичный HTTPS-адрес настроен — webhook можно подключить.' : 'На localhost мгновенные события не придут. Сначала разверните сервис и задайте PUBLIC_BASE_URL=https://ваш-домен.ru.'}</span></div>`;
  if (platform === 'vk') return `${realtimeNotice}<ol class="guide-steps">
    <li><strong>Скопируйте ссылку сообщества.</strong> Откройте своё сообщество VK и скопируйте полный адрес из строки браузера в поле «Ссылка».</li>
    <li><strong>Скопируйте ID сообщества.</strong> Откройте «Управление → Настройки → Основная информация» и вставьте числовой ID без знака минус.</li>
    <li><strong>Для расширенной статистики вставьте токен.</strong> Нужен токен пользователя-администратора с правами <code>groups</code> и <code>stats</code>. Не передавайте сервису пароль от VK.</li>
    <li><strong>Для событий откройте «Управление → Дополнительно → Работа с API → Callback API».</strong> Вставьте этот адрес сервера:${copyBox(webhook, 'Появится после настройки PUBLIC_BASE_URL')}</li>
    <li><strong>Скопируйте секретный ключ</strong> из кабинета в поле «Секретный ключ» VK:${copyBox(secret, 'Секрет не создан')}</li>
    <li><strong>Скопируйте строку подтверждения из VK</strong> в поле формы слева, сохраните форму, затем нажмите «Подтвердить» во VK. Во вкладке «Типы событий» включите новые записи, комментарии, вступления и выходы.</li>
  </ol><div class="guide-links"><a href="https://dev.vk.com/ru/api/callback/getting-started" target="_blank" rel="noopener">Официальная инструкция VK ↗</a></div>`;
  if (platform === 'telegram') return `${realtimeNotice}<ol class="guide-steps">
    <li><strong>Создайте бота.</strong> Откройте <a href="https://t.me/BotFather" target="_blank" rel="noopener">@BotFather</a>, отправьте <code>/newbot</code> и выполните его шаги.</li>
    <li><strong>Скопируйте только API token.</strong> Он выглядит как <code>123456789:AA...</code>. Вставьте его в поле «Токен бота». Никому не передавайте пароль или код входа Telegram.</li>
    <li><strong>Добавьте бота в канал.</strong> «Управление каналом → Администраторы → Добавить администратора», найдите бота и разрешите ему видеть/публиковать сообщения.</li>
    <li><strong>Укажите канал.</strong> Для публичного канала скопируйте ссылку <code>https://t.me/name</code>, а в ID вставьте <code>@name</code>. Для частного канала нужен ID вида <code>-100…</code>.</li>
    <li><strong>Сохраните форму</strong>, затем нажмите «Включить webhook». Сервис сам передаст Telegram адрес и защитный секрет:${copyBox(webhook, 'Появится после настройки PUBLIC_BASE_URL')}</li>
  </ol><button class="primary-button webhook-action" type="button" data-webhook="telegram" ${!realtimeAvailable || !config.has_token ? 'disabled' : ''}>Включить webhook Telegram</button><div class="guide-links"><a href="https://core.telegram.org/bots/features#botfather" target="_blank" rel="noopener">BotFather: официальная инструкция ↗</a><a href="https://core.telegram.org/bots/api#setwebhook" target="_blank" rel="noopener">Webhook API ↗</a></div>`;
  return `${realtimeNotice}<ol class="guide-steps">
    <li><strong>Создайте бота MAX.</strong> Нужен верифицированный профиль организации, ИП или самозанятого на платформе <a href="https://business.max.ru/self" target="_blank" rel="noopener">MAX для партнёров</a>.</li>
    <li><strong>Скопируйте токен.</strong> Откройте «Чат-боты», выберите бота, нажмите «⋮ → Настройки» и значок копирования справа от токена. Вставьте его в поле слева.</li>
    <li><strong>Сохраните форму и включите webhook.</strong> Сервис зарегистрирует защищённую подписку на события по адресу:${copyBox(webhook, 'Появится после настройки PUBLIC_BASE_URL')}</li>
    <li><strong>Добавьте бота администратором канала MAX.</strong> При событии <code>bot_added</code> сервис получит <code>chat_id</code>. Если ID уже известен, его можно сразу вставить слева.</li>
    <li><strong>Ссылка канала</strong> копируется из профиля канала в MAX и используется для публичной проверки аудитории.</li>
  </ol><button class="primary-button webhook-action" type="button" data-webhook="max" ${!realtimeAvailable || !config.has_token ? 'disabled' : ''}>Включить webhook MAX</button><div class="guide-links"><a href="https://dev.max.ru/docs/chatbots/bots-create/create" target="_blank" rel="noopener">Создание бота MAX ↗</a><a href="https://dev.max.ru/docs-api/use-cases/getting-chat-id" target="_blank" rel="noopener">Как получить chat_id ↗</a></div>`;
}

async function showConnectionHelp(platform) {
  try {
    const cabinet = state.cabinet || await loadCabinet();
    const config = cabinet.connections[platform];
    if (!config) throw new Error('Проект недоступен');
    const targetLabels = { vk: 'ID сообщества', telegram: 'ID или @username канала', max: 'chat_id канала' };
    const targetPlaceholders = { vk: 'Например, 221180361', telegram: '@my_channel или -100…', max: 'Можно оставить пустым до bot_added' };
    const tokenLabels = { vk: 'Токен доступа VK', telegram: 'Токен бота от @BotFather', max: 'Токен бота MAX' };
    document.querySelector('#connectionModalContent').innerHTML = `<div class="connection-modal-head"><span class="platform-icon ${platform}">${platformLetters[platform]}</span><div><h2>${platformLabels[platform]}</h2><p>Публичные данные + официальный API + события в реальном времени</p></div></div><div class="connection-modal-body">
      <form class="connection-form" id="connectionForm" data-platform="${platform}"><h3>Данные подключения</h3><p>Сначала добавьте ссылку. Токен можно подключить позже.</p>
        <label class="form-field"><span>Ссылка на канал или сообщество</span><input name="url" type="url" required value="${escapeHtml(config.url)}" placeholder="https://..."><small class="field-help">Скопируйте полный адрес из браузера или приложения.</small></label>
        <label class="form-field"><span>${targetLabels[platform]}</span><input name="target_id" value="${escapeHtml(config.target_id)}" placeholder="${targetPlaceholders[platform]}"></label>
        <label class="form-field input-secret"><span>${tokenLabels[platform]}</span><input name="token" type="password" autocomplete="off" placeholder="${config.has_token ? 'Токен сохранён — вставьте новый для замены' : 'Вставьте токен'}"><button type="button" data-toggle-secret>Показать</button><small class="field-help">Токен не отображается повторно и хранится только на сервере.</small></label>
        ${platform === 'vk' ? `<label class="form-field"><span>Строка подтверждения Callback API</span><input name="confirmation_code" value="${escapeHtml(config.confirmation_code)}" placeholder="Например, a1b2c3d4"><small class="field-help">Копируется из настроек Callback API вашего сообщества.</small></label>` : ''}
        <p class="form-error" id="connectionError" role="alert"></p><div class="connection-form-actions"><button class="primary-button" type="submit">Сохранить и проверить</button><button class="outline-button" type="button" data-close-connection>Отмена</button></div>
      </form><aside class="connection-guide"><h3>Что и откуда копировать</h3><p>Следуйте шагам по порядку. Все действия выполняются в официальных интерфейсах площадок.</p>${connectionGuide(platform, config, cabinet.realtime_available)}</aside></div>`;
    const modal = document.querySelector('#connectionModal');
    if (!modal.open) modal.showModal();
    bindConnectionModal(platform);
  } catch (error) {
    showToast('Не удалось открыть настройку', error.message, true);
  }
}

function bindConnectionModal(platform) {
  const modal = document.querySelector('#connectionModal');
  const form = modal.querySelector('#connectionForm');
  modal.querySelectorAll('[data-close-connection]').forEach(button => button.addEventListener('click', () => modal.close()));
  modal.querySelectorAll('[data-toggle-secret]').forEach(button => button.addEventListener('click', () => {
    const input = button.closest('.input-secret').querySelector('input');
    input.type = input.type === 'password' ? 'text' : 'password';
    button.textContent = input.type === 'password' ? 'Показать' : 'Скрыть';
  }));
  modal.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      button.textContent = 'Скопировано';
      window.setTimeout(() => { button.textContent = 'Копировать'; }, 1600);
    } catch (_) {
      showToast('Не удалось скопировать', 'Выделите значение и скопируйте его вручную.', true);
    }
  }));
  modal.querySelectorAll('[data-webhook]').forEach(button => button.addEventListener('click', async () => {
    button.disabled = true;
    const oldText = button.textContent;
    button.textContent = 'Подключаем…';
    try {
      await api('/api/connections/webhook', {
         method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ platform, folder_id: state.folderId }),
      });
      await Promise.all([loadCabinet(), renderConnections()]);
      showToast('Webhook включён', `${platformLabels[platform]} будет присылать новые события автоматически.`);
      modal.close();
    } catch (error) {
      button.disabled = false;
      button.textContent = oldText;
      showToast('Webhook не подключён', error.message, true);
    }
  }));
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const submit = form.querySelector('[type="submit"]');
    const errorNode = form.querySelector('#connectionError');
    const payload = Object.fromEntries(new FormData(form));
    payload.platform = platform;
    payload.folder_id = state.folderId;
    errorNode.textContent = '';
    submit.disabled = true;
    submit.textContent = 'Проверяем…';
    try {
      const result = await api('/api/connections/save', {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload),
      });
      await Promise.all([loadCabinet(), renderConnections(), loadDashboard()]);
      const connection = result.connections.find(item => item.id === platform);
      if (connection?.status === 'error') {
        errorNode.textContent = connection.error || 'Площадка не прошла проверку';
        showToast('Настройки сохранены', 'Проверка подключения завершилась ошибкой. Проверьте ссылку, ID и токен.', true);
      } else {
        showToast('Площадка подключена', `${platformLabels[platform]} успешно проверена.`);
        await showConnectionHelp(platform);
      }
    } catch (error) {
      errorNode.textContent = error.message;
    } finally {
      submit.disabled = false;
      submit.textContent = 'Сохранить и проверить';
    }
  });
}

async function submitAuth(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const mode = form.dataset.mode || 'login';
  const submit = form.querySelector('[type="submit"]');
  const errorNode = document.querySelector('#authError');
  const payload = Object.fromEntries(new FormData(form));
  errorNode.textContent = '';
  submit.disabled = true;
  submit.textContent = mode === 'register' ? 'Создаём…' : 'Входим…';
  try {
    await api(`/api/auth/${mode}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload),
    });
    form.reset();
    await bootstrap();
  } catch (error) {
    errorNode.textContent = error.message;
  } finally {
    submit.disabled = false;
    submit.textContent = mode === 'register' ? 'Создать кабинет' : 'Войти';
  }
}

async function logout() {
  try { await api('/api/auth/logout', { method: 'POST', body: '{}' }); } catch (_) { /* локальный выход всё равно выполняется */ }
  state.dashboard = null;
  state.account = null;
  state.cabinet = null;
  state.folderId = null;
  state.folders = [];
  // Перезапускаем приложение на корневом маршруте: так сбрасываются
  // выбранная папка, открытый раздел и возможный invite-параметр в URL.
  window.location.assign('/');
}

function exportCsv() {
  if (!state.dashboard) return;
  const rows = [['Площадка', 'Публикация', 'Дата', 'Формат', 'Охват', 'Реакции', 'Комментарии', 'ER']];
  state.dashboard.posts.forEach(post => rows.push([platformLabels[post.platform], post.title, post.date, post.type, post.reach, post.reactions, post.comments, post.er]));
  const csv = '\ufeff' + rows.map(row => row.map(cell => `"${String(cell).replaceAll('"', '""')}"`).join(';')).join('\n');
  const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
  const link = document.createElement('a');
  link.href = url; link.download = `korsakov-content-${new Date().toISOString().slice(0, 10)}.csv`; link.click();
  URL.revokeObjectURL(url);
  showToast('Экспорт готов', 'CSV-файл с публикациями загружен.');
}

function openMobileMenu() {
  document.querySelector('#sidebar').classList.add('open');
  document.querySelector('#mobileOverlay').classList.add('open');
}
function closeMobileMenu() {
  document.querySelector('#sidebar').classList.remove('open');
  document.querySelector('#mobileOverlay').classList.remove('open');
}

function bindEvents() {
  document.querySelector('#authForm').addEventListener('submit', submitAuth);
  document.querySelector('#authSwitch').addEventListener('click', () => openAuth(document.querySelector('#authForm').dataset.mode !== 'register'));
  document.querySelectorAll('[data-auth]').forEach(button => button.addEventListener('click', () => openAuth(button.dataset.auth === 'register')));
  document.querySelector('#closeAuthDialog').addEventListener('click', () => document.querySelector('#authDialog').close());
  document.querySelector('#authDialog').addEventListener('click', event => { if (event.target === event.currentTarget) event.currentTarget.close(); });
  document.querySelector('#folderSelect').addEventListener('change', event => loadFolders(event.target.value));
  document.querySelector('#renameFolder').addEventListener('click', () => renameFolder(state.folderId));
  document.querySelector('#createFolder').addEventListener('click', createFolder);
  document.querySelector('#requestFolder').addEventListener('click', () => openModal('Добавить папку', '<p>Дополнительную папку можно приобрести. Способ оплаты пока не подключён. Обратитесь к администратору сервиса, чтобы получить доступ к дополнительной папке.</p>'));
  document.querySelectorAll('.nav-item').forEach(button => button.addEventListener('click', () => navigate(button.dataset.page)));
  document.querySelectorAll('[data-go]').forEach(button => button.addEventListener('click', () => navigate(button.dataset.go)));
  document.querySelectorAll('.platform-nav button').forEach(button => button.addEventListener('click', () => {
    state.contentPlatform = button.dataset.filter;
    document.querySelectorAll('#contentFilters button').forEach(chip => chip.classList.toggle('active', chip.dataset.platform === state.contentPlatform));
    renderContent(); navigate('content');
  }));
  document.querySelector('#periodSelect').addEventListener('change', event => { state.period = Number(event.target.value); loadDashboard(); });
  document.querySelectorAll('.chart-tabs button').forEach(button => button.addEventListener('click', () => {
    state.metric = button.dataset.metric;
    document.querySelectorAll('.chart-tabs button').forEach(tab => tab.classList.toggle('active', tab === button));
    renderChart();
  }));
  document.querySelector('#syncButton').addEventListener('click', event => syncAll(event.currentTarget));
  document.querySelector('#syncAll').addEventListener('click', event => syncAll(event.currentTarget));
  document.querySelector('#contentSearch').addEventListener('input', event => { state.search = event.target.value; renderContent(); });
  document.querySelectorAll('#contentFilters button').forEach(button => button.addEventListener('click', () => {
    state.contentPlatform = button.dataset.platform;
    document.querySelectorAll('#contentFilters button').forEach(chip => chip.classList.toggle('active', chip === button));
    renderContent();
  }));
  document.querySelector('#sortEr').addEventListener('click', () => { state.sortDesc = !state.sortDesc; renderContent(); });
  document.querySelector('#sortErMobile').addEventListener('click', () => { state.sortDesc = !state.sortDesc; renderContent(); });
  document.querySelector('#exportContent').addEventListener('click', exportCsv);
  document.querySelector('#openHelp').addEventListener('click', () => openModal('Как подключить площадки', setupContent()));
  document.querySelector('#showSetup').addEventListener('click', () => openModal('Безопасная настройка', setupContent()));
  document.querySelector('#openSettings').addEventListener('click', () => navigate('connections'));
  document.querySelector('#logoutButton').addEventListener('click', logout);
  document.querySelector('#moreInsights').addEventListener('click', () => openModal('Рекомендации KORSAKOV', '<p>Алгоритм сравнил площадки и нашёл три точки роста.</p><ol><li>Публикуйте гайды в MAX дважды в неделю.</li><li>Перенесите ключевые посты Telegram в окно 10:00–12:00.</li><li>Используйте короткий лид до 140 символов во ВКонтакте.</li></ol>'));
  document.querySelector('#currentGrouping').addEventListener('change', () => loadHistorySection('current'));
  document.querySelector('#archiveGrouping').addEventListener('change', () => loadHistorySection('archive'));
  document.querySelector('#archiveYear').addEventListener('change', event => { state.archiveYear = Number(event.target.value); loadHistorySection('archive'); });
  document.querySelector('#currentVkBackfill').addEventListener('click', () => backfillVk('current'));
  document.querySelector('#archiveVkBackfill').addEventListener('click', () => backfillVk('archive'));
  document.querySelector('#closeModal').addEventListener('click', () => document.querySelector('#infoModal').close());
  document.querySelector('#closeConnectionModal').addEventListener('click', () => document.querySelector('#connectionModal').close());
  document.querySelector('#infoModal').addEventListener('click', event => { if (event.target === event.currentTarget) event.currentTarget.close(); });
  document.querySelector('#connectionModal').addEventListener('click', event => { if (event.target === event.currentTarget) event.currentTarget.close(); });
  document.querySelector('#menuButton').addEventListener('click', openMobileMenu);
  document.querySelector('#mobileOverlay').addEventListener('click', closeMobileMenu);
}

hydrateIcons();
bindEvents();
bootstrap();
