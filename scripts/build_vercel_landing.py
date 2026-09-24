"""Build a public landing without exposing an unconfigured account backend."""

from pathlib import Path
import re
import shutil

root = Path(__file__).resolve().parent.parent
source = root / "app"
target = root / "vercel-site"
target.mkdir(exist_ok=True)

for asset in ("styles.css", "favicon.svg", "korsakov-mark.svg"):
    shutil.copyfile(source / asset, target / asset)

page = (source / "index.html").read_text(encoding="utf-8")
start = page.index('  <section class="public-site"')
end = page.index('    <dialog class="auth-dialog"', start)
landing = page[start:end].rstrip()

landing = re.sub(
    r'<button class="landing-text-button" data-auth="login">Войти</button>',
    '<a class="landing-text-button" href="#launch">О запуске</a>',
    landing,
)
landing = re.sub(
    r'<button class="([^"]*landing-button[^"]*)" data-auth="register">(?:Создать аккаунт|Начать работу) <span aria-hidden="true">↗</span></button>',
    r'<a class="\1" href="#launch">О запуске кабинета <span aria-hidden="true">↗</span></a>',
    landing,
)
landing = landing.replace(
    '<span class="landing-smallprint">1 папка бесплатно · 3 соцсети · ваши данные отдельно</span>',
    '<span class="landing-smallprint">Публичная страница KORSAKOV · кабинет готовится к запуску</span>',
)
landing = landing.replace(
    '<span>Первая папка доступна бесплатно</span>',
    '<span>Регистрация откроется после подключения постоянного хранилища</span>',
)
landing = landing.replace(
    '    </main><footer',
    '      <section class="landing-container launch-note" id="launch"><h2>Кабинет готовится к запуску</h2><p>Публичная страница уже доступна. Регистрация, подключения и история появятся здесь после переноса данных в постоянное хранилище.</p></section>\n    </main><footer',
)
landing += "\n  </section>"
head = page[:start].replace('<body>', '<body class="vercel-landing">')
(target / "index.html").write_text(head + landing + "\n</body>\n</html>\n", encoding="utf-8")

with (target / "styles.css").open("a", encoding="utf-8") as css:
    css.write("\n.launch-note { padding-block: 20px 70px; text-align: center; }\n")
    css.write(".launch-note h2 { font-size: clamp(25px, 3vw, 40px); }\n")
    css.write(".launch-note p { max-width: 620px; margin: 0 auto; color: #68717f; line-height: 1.7; }\n")
    css.write(".vercel-landing .landing-text-button { text-decoration: none; }\n")

assert 'data-auth=' not in landing
assert '<form' not in landing
print("Built", target)
