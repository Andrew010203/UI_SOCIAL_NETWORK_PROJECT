from fixtures.ui_fixtures import *



def pytest_terminal_summary(terminalreporter):
   """
   Хук pytest, выполняющийся после завершения всех тестов.
   Собирает статистику по результатам и отправляет сводку в Telegram.
   """
   load_dotenv()
   # Токен бота Telegram для отправки сообщений
   TOKEN = os.getenv("TOKEN")
   # Идентификатор чата в Telegram, куда отправлять результаты
   CHAT_ID = os.getenv("CHAT_ID")
   repo_name = os.getenv("GITHUB_REPOSITORY")  # формат "user/repo"
   run_id = os.getenv("GITHUB_RUN_ID")
   # Проверяем, реально ли мы в облаке GitHub Actions
   is_github_actions = os.getenv("GITHUB_ACTIONS") == "true"
   if is_github_actions:
       repo_name = os.getenv("GITHUB_REPOSITORY")
       full_name = repo_name
       user, repo = full_name.split("/")

       # Пока деплой не настроен на подпапки, используем корень:
       GITHUB_PAGE_URL = f"https://{user.lower()}.github.io/{repo}/"
   else:
       # Локально
       GITHUB_PAGE_URL = "https://andrew010203.github.io"

   config = terminalreporter.config
   if hasattr(config, "workerinput"):
       return
   # Фиксируем время запуска сборки (под конец, хотя обычно это начало)
   start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   # Структура для хранения агрегированных результатов по каждому файлу тестов
   suite_results = {
       # заранее задаём для одного набора, можно расширять динамически

   }
   # Проходим по всем результатам, которые pytest сохранил в terminalreporter.stats
   for outcome, reports in terminalreporter.stats.items():
       for report in reports:
           # report.nodeid выглядит как: test_users.py::TestUser::test_create_user
           suite_name = report.nodeid.split("::")[0]  # вытаскиваем только имя файла тестов
           # Если встретился новый файл тестов, инициализируем для него счётчики
           if suite_name not in suite_results:
               suite_results[suite_name] = {"passed": 0, "failed": 0, "skipped": 0, "errors": 0}
           # Увеличиваем соответствующий счётчик
           if outcome == "passed":
               suite_results[suite_name]["passed"] += 1
           elif outcome == "failed":
               suite_results[suite_name]["failed"] += 1
           elif outcome == "skipped":
               suite_results[suite_name]["skipped"] += 1
           elif outcome == "error":
               suite_results[suite_name]["errors"] += 1
   # Формируем текст сообщения для Telegram
   message = f"*РЕЗУЛЬТАТЫ ТЕСТОВ:*\n\n *Время запуска:* {start_time}"
   for suite, results in suite_results.items():
       message += (
           f" *Набор тестов:* '{suite}'\n"
           f"✅ *Пройдено:* {results['passed']}\n"
           f"❌ *Не пройдено:* {results['failed']}\n"
           f"⏭ *Пропущено:* {results['skipped']}\n"
           f"⚠ *Ошибки:* {results['errors']}\n"
           f"-----------------------------\n\n"
       )
   # Добавляем ссылку на Github
   message += f"[Подробнее на Github Pages]({GITHUB_PAGE_URL})"
   # Добавляем конструкцию для отладки
   print(f"\n--- DEBUG INFO ---")
   print(f"TOKEN exists: {bool(TOKEN)}")
   print(f"CHAT_ID exists: {bool(CHAT_ID)}")
   print(f"GITHUB_ACTIONS: {os.getenv('GITHUB_ACTIONS')}")
   print(f"URL: {GITHUB_PAGE_URL}")
   print(f"------------------\n")
   try:
       # Отправляем POST-запрос к Telegram Bot API
       response = requests.post(
           url=f"https://api.telegram.org/bot{TOKEN}/sendMessage",
           headers={"Content-Type": "application/json"},
           json={
               "chat_id": CHAT_ID,
               "text": message,
               "parse_mode": "HTML",
               "disable_web_page_preview": True
           }
       )
       # Проверяем, нет ли ошибок в ответе
       response.raise_for_status()
   except requests.RequestException as e:
       # Если запрос не удался, выводим содержимое ответа для отладки
       if e.response is not None:
           print("Ответ Телеграмма:", e.response.json())