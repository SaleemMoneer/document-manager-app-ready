import firebase_admin
from firebase_admin import credentials, firestore
import os
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk
import time

cred = credentials.Certificate("documentmanagerapp.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_name = "documents"

def add_document(title, content, category):
    if not title:
        messagebox.showerror("خطأ", "العنوان مطلوب!")
        return
    doc = {
        "title": title,
        "content": content if content else None,
        "category": category if category else None,
        "created_at": firestore.SERVER_TIMESTAMP,
    }
    db.collection(collection_name).add(doc)
    messagebox.showinfo("تم", "تم حفظ المستند.")

def show_documents():
    docs = db.collection(collection_name).order_by("created_at").stream()
    output = ""
    for doc in docs:
        data = doc.to_dict()
        output += f"\n📄 رقم: {doc.id}\nالعنوان: {data.get('title')}\nالتصنيف: {data.get('category')}\n---\n"
    if output:
        show_output("عرض المستندات", output)
    else:
        messagebox.showinfo("تنبيه", "لا توجد مستندات.")

def search_documents():
    keyword = simpledialog.askstring("بحث", "أدخل كلمة البحث:")
    if not keyword:
        return
    start = time.time()
    docs = db.collection(collection_name).stream()
    output = ""
    for doc in docs:
        data = doc.to_dict()
        if keyword.lower() in (data.get("title", "") + data.get("content", "")).lower():
            output += f"\n📄 رقم: {doc.id}\nالعنوان: {data.get('title')}\nالمحتوى: {data.get('content')}\n---\n"
    if output:
        duration = time.time() - start
        show_output("نتائج البحث", output + f"\n⏱️ {duration:.2f} ثانية")
    else:
        messagebox.showinfo("نتائج البحث", "لا توجد نتائج.")

def delete_document():
    doc_id = simpledialog.askstring("حذف مستند", "أدخل رقم المستند:")
    if not doc_id:
        return
    try:
        db.collection(collection_name).document(doc_id).delete()
        messagebox.showinfo("تم", "تم حذف المستند.")
    except:
        messagebox.showerror("خطأ", "حدث خطأ أثناء الحذف.")

def update_document():
    doc_id = simpledialog.askstring("تعديل", "أدخل رقم المستند:")
    if not doc_id:
        return
    doc_ref = db.collection(collection_name).document(doc_id)
    doc = doc_ref.get()
    if not doc.exists:
        messagebox.showerror("خطأ", "لا يوجد مستند بهذا الرقم.")
        return
    data = doc.to_dict()
    new_title = simpledialog.askstring("عنوان جديد", "أدخل العنوان الجديد:", initialvalue=data.get("title"))
    new_content = simpledialog.askstring("محتوى جديد", "أدخل المحتوى الجديد:", initialvalue=data.get("content"))
    new_category = simpledialog.askstring("تصنيف جديد", "أدخل التصنيف الجديد:", initialvalue=data.get("category"))
    doc_ref.update({"title": new_title, "content": new_content, "category": new_category})
    messagebox.showinfo("تم", "تم تحديث المستند.")

def show_statistics():
    docs = db.collection(collection_name).stream()
    count = 0; total = 0
    for d in docs:
        data = d.to_dict(); count += 1
        total += sum(len(str(v)) for v in data.values())
    messagebox.showinfo("الإحصاءات", f"عدد المستندات: {count}\nحجم تقريبي: {total/1024:.2f} KB")

def add_documents_from_folder():
    folder = filedialog.askdirectory()
    if not folder:
        return
    added = 0
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
                content = f.read()
                doc = {
                    "title": os.path.splitext(filename)[0],
                    "content": content,
                    "category": "مجلد محلي",
                    "created_at": firestore.SERVER_TIMESTAMP
                }
                db.collection(collection_name).add(doc); added += 1
    messagebox.showinfo("تم", f"تم تحميل {added} مستند.")

def show_output(title, content):
    win = tk.Toplevel(root)
    win.title(title)
    t = tk.Text(win, wrap='word')
    t.insert('1.0', content)
    t.pack(expand=True, fill='both')

root = tk.Tk()
root.title("نظام إدارة المستندات")
root.geometry("400x500")

buttons = [
    ("إضافة مستند", lambda: add_document(
        simpledialog.askstring("عنوان", "أدخل العنوان:"),
        simpledialog.askstring("محتوى", "أدخل المحتوى:"),
        simpledialog.askstring("تصنيف", "أدخل التصنيف:"))),
    ("عرض المستندات", show_documents),
    ("بحث", search_documents),
    ("حذف", delete_document),
    ("تعديل", update_document),
    ("إحصاءات", show_statistics),
    ("استيراد", add_documents_from_folder),
    ("خروج", root.quit)
]

for txt, cmd in buttons:
    ttk.Button(root, text=txt, command=cmd).pack(fill='x', padx=20, pady=5)

root.mainloop()
