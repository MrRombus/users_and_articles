import sqlite3
import logging
from tkinter import Button, Label, Entry, Tk, Listbox, StringVar, Text, END, BOTH, messagebox, Toplevel
from tkinter.ttk import Frame

import article.logg
from article.article import ArticleStorage

class AddUserWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        self.title('Добавить')
        self.lbl_add_user = Label(self, text='Добавить пользователя: ')
        self.lbl_add_user.grid(row=0, column=0)

        self.lbl_nickname = Label(self, text='Никнейм:')
        self.lbl_nickname.grid(row=1, column=0)

        self.entry_nickname = Entry(self)
        self.entry_nickname.grid(row=1, column=1)

        self.lbl_name = Label(self, text='Имя:')
        self.lbl_name.grid(row=2, column=0)

        self.entry_name = Entry(self)
        self.entry_name.grid(row=2, column=1)

        self.lbl_surname = Label(self, text='Фамилия:')
        self.lbl_surname.grid(row=3, column=0)

        self.entry_surname = Entry(self)
        self.entry_surname.grid(row=3, column=1)

        self.btn_add_user = Button(self, text='Добавить', bg='green', command=self.add_user)
        self.btn_add_user.grid(row=4, column=0)


    def add_user(self):
        nickname = self.entry_nickname.get()
        name = self.entry_name.get()
        surname = self.entry_surname.get()

        if self.parent._article_storage.add_user(nickname, name, surname):
            self.parent._fill_lb(self.parent.lb_users, self.parent._article_storage.get_users(), ['Все'])
            messagebox.showinfo('Info', f'Пользователь {nickname} добавлен в базу')
            self.destroy()
        else:
            messagebox.showerror('Error', f'Пользователь {nickname} не может быть добавлен')
        
        self.entry_nickname.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_surname.delete(0, END)

class EditUserWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.old_surname = None
        self.old_nickname = None
        self.old_name = None
        self.initUI()

    def initUI(self):
        self.title('Изменить')
        self.lbl_ed_user = Label(self, text='Изменить пользователя: ')
        self.lbl_ed_user.grid(row=0, column=0)

        self.lbl_nickname = Label(self, text='Никнейм:')
        self.lbl_nickname.grid(row=1, column=0)

        self.entry_nickname = Entry(self)
        #self.entry_nickname.insert(0, self.old_nickname)
        self.entry_nickname.grid(row=1, column=1)

        self.lbl_name = Label(self, text='Имя:')
        self.lbl_name.grid(row=2, column=0)

        self.entry_name = Entry(self)
        self.entry_name.grid(row=2, column=1)

        self.lbl_surname = Label(self, text='Фамилия:')
        self.lbl_surname.grid(row=3, column=0)

        self.entry_surname = Entry(self)
        self.entry_surname.grid(row=3, column=1)

        self.btn_ed_user = Button(self, text='Изменить', bg='yellow', command=self.ed_user)
        self.btn_ed_user.grid(row=4, column=0)

    def ed_user(self):
        nickname = self.parent._selected_user
        new_nickname = self.entry_nickname.get()
        new_name = self.entry_name.get()
        new_surname = self.entry_surname.get()

        if self.parent._article_storage.edit_user(nickname, new_nickname, new_name, new_surname):
            self.parent._fill_lb(self.parent.lb_users, self.parent._article_storage.get_users(), ['Все'])
            messagebox.showinfo('Info', f'Пользователь {nickname} был изменён')
            self.destroy()
        else:
            messagebox.showerror('Error', f'Пользователь {nickname} не может быть изменён')
        
        self.entry_nickname.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_surname.delete(0, END)




class ArticleWindow(Frame):
    def __init__(self, article_storage):
        super().__init__()
        self._article_storage = article_storage
        self._selected_user = None
        self._selected_article = None
        self.initUI()

    def setGeometry(self, w=600, h=450):
        self.master.geometry(f'{w}x{h}')

    def initUI(self):
        self.master.title("Список")

        users = self._article_storage.get_users()

        articles = self._article_storage.get_articles()

        lbl_users = Label(self, text='Пользователи: ')
        lbl_users.grid(row=0, column=0)

        self.lb_users = Listbox(self)

        self._fill_lb(self.lb_users, users, ['Все'])

        self.lb_users.bind("<<ListboxSelect>>", self.onSelect)

        # lb_users.pack(side=LEFT, padx=15)
        self.lb_users.grid(row=1, column=0, padx=15)

        lbl_articles = Label(self, text='Статьи: ')
        lbl_articles.grid(row=0, column=1)

        self.lb_articles = Listbox(self)

        self._fill_lb(self.lb_articles, articles)

        self.lb_articles.bind("<<ListboxSelect>>", self.onSelect_2)

        self.lb_articles.grid(row=1, column=1)

        lbl_text = Label(self, text='Текст статьи: ')
        lbl_text.grid(row=0, column=2)

        self.txt_text = Text(self, width=25, height=10)
        self.txt_text.grid(row=1, column=2)

        self.var = StringVar()
        self.label_user = Label(self, text=0, textvariable=self.var)
        self.label_user.grid(row=2, column=0)

        self.var_2 = StringVar()
        self.label_article = Label(self, text=0, textvariable=self.var_2)
        self.label_article.grid(row=2, column=1)

        self.pack(fill=BOTH, padx=15)

        self.btn_add_user = Button(self, text='Добавить', bg='green', command=self.add_user)
        self.btn_add_user.grid(row=7, column=0)

        self.btn_add_user = Button(self, text='Изменить', bg='yellow', command=self.ed_user)
        self.btn_add_user.grid(row=8, column=0)

        self.btn_del_user = Button(self, text='Удалить', bg='red', command=self.del_user)
        self.btn_del_user.grid(row=9, column=0)

        self.btn_edit_article = Button(self, text='Редактировать Статью', bg='yellow', command=self.ed_article)
        self.btn_edit_article.grid(row=7, column=1)

        self.btn_del_article = Button(self, text='Удалить Статью', bg='red', command=self.del_article)
        self.btn_del_article.grid(row=8, column=1)


    def onSelect(self, val):
        sender = val.widget
        idx = sender.curselection()
        username = sender.get(idx)

        if username.lower() == 'все':
            self._fill_lb(self.lb_articles, self._article_storage.get_articles())
        else:
            self._fill_lb(self.lb_articles, self._article_storage.get_articles(username))

        self.var.set(username)
        self._selected_user = username

    def onSelect_2(self, val):
        sender = val.widget
        idx = sender.curselection()
        headline = sender.get(idx)

        text = self._article_storage.get_article_text(headline)
        self._fill_txt(self.txt_text, text)

        self.var_2.set(headline)
        self._selected_article = headline

    def add_user(self):
        add_user_window = AddUserWindow(self)
        add_user_window.grab_set()

    def ed_user(self):
        edit_user_window = EditUserWindow(self)
        edit_user_window.grab_set()

    def del_user(self):
        if self._selected_user:
            nickname = self._selected_user
            res = messagebox.askokcancel('Вопрос', 'Вы уверены?')

            if res:
                if self._article_storage.delete_user(nickname):
                    self._fill_lb(self.lb_users, self._article_storage.get_users(), ['Все'])
                    messagebox.showinfo('Info', f'Пользователь {nickname} был удалён')
                else:
                    messagebox.showerror('Error', f'Пользователь {nickname} не может быть удалён')
            else:
                messagebox.showinfo('Info', f'Пользователь {nickname} не был удалён')
        else:
            messagebox.showerror('Error', f'Пользователь не выбран')
        
    def del_article(self):
        if self._selected_article:
            headline = self._selected_article
            res = messagebox.askokcancel('Вопрос', 'Вы уверены?')

            if res:
                if self._article_storage.delete_article(headline):
                    self._fill_lb(self.lb_articles, self._article_storage.get_articles())
                    messagebox.showinfo('Info', f'Статья {headline} была удалена')
                else:
                    messagebox.showerror('Error', f'Статья {headline} не может быть удалена')
            else:
                messagebox.showinfo('Info', f'Статья {headline} не удалена')
        else:
            messagebox.showerror('Error', f'Статья не выбрана')

    def ed_article(self):
        if self._selected_article:
            headline = self._selected_article
            text = self.txt_text.get("1.0","end")
            res = messagebox.askokcancel('Вопрос', 'Вы уверены?')

            if res:
                if self._article_storage.edit_article(headline, text):
                    messagebox.showinfo('Info', f'Статья {headline} была изменена')
                else:
                    messagebox.showerror('Error', f'Статья {headline} не может быть изменена')
            else:
                messagebox.showinfo('Info', f'Статья {headline} не изменена')
        else:
            messagebox.showerror('Error', f'Статья не выбрана')

    def _fill_lb(self, lb, items, extra=[]):
        lb.delete(0, END)
        for item in items:
            lb.insert(END, item)
        if extra:
            for item in extra:
                lb.insert(END, item)

    def _fill_txt(self, txt, text):
        txt.delete(1.0, END)
        txt.insert(END, text)


if __name__ == '__main__':
    root = Tk()

    conn = sqlite3.connect('article/ArticleStorage.sqlite3')
    u_storage_log = logging.getLogger('u_storage')

    article_storage = ArticleStorage(conn, u_storage_log)

    article_window = ArticleWindow(article_storage)
    article_window.setGeometry()

    root.mainloop()
