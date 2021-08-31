import discord,sqlite3,asyncio

print(asyncio.all_tasks)


def voice(ip : str):
    #cancel voice task function
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute(f"SELECT task FROM voice WHERE ip = '{ip}'")
    task_name = c.fetchone()
    conn.commit()
    if task_name is None:
        return False

    _task = [tasks for tasks in asyncio.all_tasks() if tasks.get_name() == task_name[0]]
    print(_task)

    #try:
    if _task is not None:
        _task[0].cancel()
        return True
    elif _task is None:
        return False