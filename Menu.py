from tkinter import *

def menu_bar(rodzic, stan, nowa, otworz,
    show_workers, worker_add, worker_edit, worker_delete,
    show_work_1, add_work_1, add_column_work_1, work_1_edit, work_1_delete,
    show_work_2, add_work_2, add_column_work_2, work_2_edit, work_2_delete,
    print_to_txt, print_to_pdf,
    show_history):
    """wyświetlanie paska menu"""

    global show_r, menu, m_plik

    if stan == 1:

        menu = Menu(rodzic)

        rodzic.config(menu=menu)
        m_plik = Menu(menu, activebackground="black", activeforeground="white", tearoff=0)
        show_r = Menu(menu, activebackground="black", activeforeground="white",tearoff=0)
        add_r = Menu(menu, activebackground="black", activeforeground="white",tearoff=0)
        edit_r = Menu(menu, activebackground="black", activeforeground="white",tearoff=0)
        rem_r = Menu(menu, activebackground="black", activeforeground="white",tearoff=0)

        menu.add_cascade(label="Plik", menu=m_plik)
        m_plik.add_command(label="Nowy", command=nowa)
        m_plik.add_command(label="Otwórz", command=otworz)
        m_plik.add_separator()
        m_plik.add_command(label="Historia zmian", command=show_history, state=DISABLED)
        m_plik.add_separator()
        m_plik.add_command(label="Wydrukuj do txt", command=print_to_txt, state=DISABLED)
        m_plik.add_command(label="Wydrukuj do pdf", command=print_to_pdf, state=DISABLED)
        m_plik.add_separator()
        m_plik.add_command(label="Exit", command=rodzic.quit)

        menu.add_cascade(label="Wyświetl ...", menu=show_r, state=DISABLED)
        show_r.add_command(label="tabele pracowników", command=show_workers)
        show_r.add_separator()
        show_r.add_command(label="tabele zwijania", command=show_work_1)
        show_r.add_separator()
        show_r.add_command(label="tabele prasa", command=show_work_2)

        menu.add_cascade(label="Dodaj wpis ...", menu=add_r, state=DISABLED)
        add_r.add_command(label="do bazy pracownika", command=worker_add)
        add_r.add_separator()
        add_r.add_command(label="do bazy zwijania", command=add_work_1)
        add_r.add_command(label="do bazy prasa", command=add_work_2)
        add_r.add_command(label="Dodaj kolumne", command=add_column_work_2)

        menu.add_cascade(label="Edytuj wpis ...", menu=edit_r, state=DISABLED)
        edit_r.add_command(label="w bazie pracowników", command=lambda: worker_edit(1))
        edit_r.add_separator()
        edit_r.add_command(label="w bazie zwijanie", command=lambda: work_1_edit(1))
        edit_r.add_separator()
        edit_r.add_command(label="w bazie prasa", command=lambda: work_2_edit(1))

        menu.add_cascade(label="Usuń wpis ...", menu=rem_r, state=DISABLED)
        rem_r.add_command(label="z bazy pracowników", command=lambda: worker_delete(2))
        rem_r.add_separator()
        rem_r.add_command(label="z bazy zwijania", command=lambda: work_1_delete(2))
        rem_r.add_separator()
        rem_r.add_command(label="z bazy prasa", command=lambda: work_2_delete(2))

    elif stan == 2:

        m_plik.entryconfigure(0, state='disabled')
        m_plik.entryconfigure(1, state='disabled')

        m_plik.entryconfigure(3, state='normal')
        m_plik.entryconfigure(5, state='normal')
        m_plik.entryconfigure(6, state='normal')

        menu.entryconfigure(2, state='normal')
        menu.entryconfigure(3, state='normal')
        menu.entryconfigure(4, state='normal')
        menu.entryconfigure(5, state='normal')


