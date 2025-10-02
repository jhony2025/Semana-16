#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación GUI para Gestión de Tareas con Atajos de Teclado
Autor: (estudiante) - ejemplo basado en conceptos de GUI, OOP y manejo de eventos
Requisitos implementados:
 - Tkinter GUI (Entry, Buttons, Treeview)
 - Añadir tareas (botón + Enter)
 - Marcar como completada (botón, tecla 'c', doble clic)
 - Eliminar tarea (botón, tecla 'Delete' o 'd')
 - Cerrar con Escape
 - Feedback visual (tareas completadas gris + tachado)
 - Persistencia simple a tasks.json (guardar/cargar) con manejo de excepciones
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, font

TASKS_FILE = "tasks.json"

class Task:
    """Modelo simple para una tarea."""
    def __init__(self, text: str, completed: bool = False):
        self.text = text
        self.completed = completed

    def to_dict(self):
        return {"text": self.text, "completed": self.completed}

    @staticmethod
    def from_dict(d):
        return Task(d.get("text", ""), d.get("completed", False))


class TaskManagerApp:
    """Clase principal de la aplicación que encapsula la GUI y la lógica."""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Gestión de Tareas - GPT Español")
        self.root.geometry("600x400")
        self.root.minsize(480, 320)

        # Lista interna de tareas (colección)
        self.tasks = []

        # Fonts
        self.font_regular = font.Font(family="Helvetica", size=10)
        self.font_completed = font.Font(family="Helvetica", size=10, overstrike=1)

        # Construir interfaz
        self._build_ui()

        # Cargar tareas desde archivo (manejo de archivos y excepciones)
        self.load_tasks()

        # Bindings de teclado (escuchadores de eventos)
        self.root.bind("<Escape>", lambda e: self.on_escape())
        # Bind para 'c' y 'C' (marcar completada)
        self.root.bind_all("<Key-c>", lambda e: self.mark_selected_completed())
        self.root.bind_all("<Key-C>", lambda e: self.mark_selected_completed())
        # Bind para 'd' y 'D' (eliminar)
        self.root.bind_all("<Key-d>", lambda e: self.delete_selected_task())
        self.root.bind_all("<Key-D>", lambda e: self.delete_selected_task())
        # Bind Delete key
        self.root.bind_all("<Delete>", lambda e: self.delete_selected_task())

    def _build_ui(self):
        # --- Contenedor superior: entrada y botones ---
        top_frame = ttk.Frame(self.root, padding=(10, 8))
        top_frame.pack(side=tk.TOP, fill=tk.X)

        # Entry para nueva tarea
        self.entry_task = ttk.Entry(top_frame, font=self.font_regular)
        self.entry_task.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        # Cuando el usuario presione Enter en el Entry -> añadir tarea
        self.entry_task.bind("<Return>", lambda e: self.add_task())

        # Botón añadir
        btn_add = ttk.Button(top_frame, text="Añadir (Enter)", command=self.add_task)
        btn_add.pack(side=tk.LEFT, padx=(0, 6))

        # Botón marcar completada
        btn_complete = ttk.Button(top_frame, text="Marcar como completada (C)", command=self.mark_selected_completed)
        btn_complete.pack(side=tk.LEFT, padx=(0, 6))

        # Botón eliminar
        btn_delete = ttk.Button(top_frame, text="Eliminar (Delete / D)", command=self.delete_selected_task)
        btn_delete.pack(side=tk.LEFT)

        # --- Árbol/Lista de tareas ---
        middle_frame = ttk.Frame(self.root, padding=(10, 6))
        middle_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("task",)
        self.tree = ttk.Treeview(middle_frame, columns=columns, show="tree", selectmode="browse")
        # Scrollbars
        vsb = ttk.Scrollbar(middle_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar tags para estilo visual
        self.tree.tag_configure("pending", foreground="black", font=self.font_regular)
        self.tree.tag_configure("completed", foreground="gray40", font=self.font_completed)

        # Doble clic en item => toggle completado
        self.tree.bind("<Double-1>", lambda e: self.toggle_selected_completed())

        # --- Panel inferior: estado y guardado ---
        bottom_frame = ttk.Frame(self.root, padding=(10, 6))
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.lbl_status = ttk.Label(bottom_frame, text="Tareas: 0 | Pendientes: 0 | Completadas: 0")
        self.lbl_status.pack(side=tk.LEFT)

        btn_save = ttk.Button(bottom_frame, text="Guardar", command=self.save_tasks)
        btn_save.pack(side=tk.RIGHT)

        btn_load = ttk.Button(bottom_frame, text="Cargar", command=self.load_tasks)
        btn_load.pack(side=tk.RIGHT, padx=(0,6))

        # Instrucciones rápidas
        help_text = "Atajos: Enter=añadir, C=marcar completada, D/Delete=eliminar, Esc=cerrar"
        self.lbl_help = ttk.Label(bottom_frame, text=help_text, foreground="gray30")
        self.lbl_help.pack(side=tk.RIGHT, padx=(0,12))

    # ---------- Métodos principales ----------
    def add_task(self):
        text = self.entry_task.get().strip()
        if not text:
            messagebox.showwarning("Entrada vacía", "Escribe una descripción para la tarea antes de añadirla.")
            return
        task = Task(text=text, completed=False)
        self.tasks.append(task)
        self._insert_task_in_tree(task)
        self.entry_task.delete(0, tk.END)
        self.update_status()

    def _insert_task_in_tree(self, task: Task):
        tag = "completed" if task.completed else "pending"
        # Use text as displayed node
        self.tree.insert("", tk.END, text=task.text, tags=(tag,))

    def get_selected_index(self):
        sel = self.tree.selection()
        if not sel:
            return None
        # Map selection id to index in self.tasks by comparing text and completed flag.
        # Note: if tasks can repeat text, we choose mapping by position: traverse tree children.
        sel_id = sel[0]
        children = self.tree.get_children()
        try:
            idx = children.index(sel_id)
            return idx
        except ValueError:
            return None

    def mark_selected_completed(self):
        idx = self.get_selected_index()
        if idx is None:
            # No selection -> mostrar advertencia pero no interrumpir flujo
            # Usamos un messagebox leve (info).
            messagebox.showinfo("Selecciona una tarea", "Selecciona primero la tarea que deseas marcar como completada (clic en la tarea).")
            return
        # Alternar estado (si ya está completada la dejamos tal cual para "marcar como completada")
        self.tasks[idx].completed = True
        # Actualizar Treeview (reconfigurar tag)
        item_id = self.tree.get_children()[idx]
        self.tree.item(item_id, text=self.tasks[idx].text, tags=("completed",))
        self.update_status()

    def toggle_selected_completed(self):
        """Doble clic togglea estado completada / pendiente."""
        idx = self.get_selected_index()
        if idx is None:
            return
        self.tasks[idx].completed = not self.tasks[idx].completed
        item_id = self.tree.get_children()[idx]
        tag = "completed" if self.tasks[idx].completed else "pending"
        self.tree.item(item_id, text=self.tasks[idx].text, tags=(tag,))
        self.update_status()

    def delete_selected_task(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showinfo("Selecciona una tarea", "Selecciona la tarea que deseas eliminar.")
            return
        # Confirmación
        task_text = self.tasks[idx].text
        if not messagebox.askyesno("Confirmar eliminación", f"¿Eliminar la tarea:\n\n{task_text}\n\n?"):
            return
        # Eliminar de estructura y Treeview
        item_id = self.tree.get_children()[idx]
        self.tree.delete(item_id)
        del self.tasks[idx]
        self.update_status()

    def update_status(self):
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed
        self.lbl_status.config(text=f"Tareas: {total} | Pendientes: {pending} | Completadas: {completed}")

    # ---------- Persistencia ----------
    def save_tasks(self):
        # Guardar self.tasks en JSON
        try:
            data = [t.to_dict() for t in self.tasks]
            with open(TASKS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Guardado", f"Tareas guardadas en '{TASKS_FILE}'.")
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo guardar las tareas:\n{e}")

    def load_tasks(self):
        # Cargar desde JSON (si existe)
        if not os.path.exists(TASKS_FILE):
            # No existe archivo -> iniciar limpio
            self.tasks = []
            self._refresh_tree()
            self.update_status()
            return
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            loaded = []
            for item in data:
                try:
                    loaded.append(Task.from_dict(item))
                except Exception:
                    # Ignorar elementos mal formados
                    continue
            self.tasks = loaded
            self._refresh_tree()
            self.update_status()
            messagebox.showinfo("Cargado", f"Tareas cargadas desde '{TASKS_FILE}'.")
        except Exception as e:
            messagebox.showerror("Error al cargar", f"No se pudo cargar las tareas:\n{e}")

    def _refresh_tree(self):
        # Limpiar y reinsertar
        for child in self.tree.get_children():
            self.tree.delete(child)
        for task in self.tasks:
            self._insert_task_in_tree(task)

    # ---------- Eventos de ventana ----------
    def on_escape(self):
        if messagebox.askyesno("Salir", "¿Deseas cerrar la aplicación?"):
            self.root.destroy()


def main():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
