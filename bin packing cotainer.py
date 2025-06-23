import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class BinPackingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Logistics Packing System")
        
        # Variables
        self.items = []
        self.bins = []
        self.max_volume = tk.DoubleVar(value=10.0)
        self.max_weight = tk.DoubleVar(value=15.0)
        
        # GUI Layout
        self.setup_input_frame()
        self.setup_results_frame()
    
    def setup_input_frame(self):
        input_frame = ttk.LabelFrame(self.root, text="Item Input", padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        # Item Input
        ttk.Label(input_frame, text="Volume (m³):").grid(row=0, column=0)
        self.vol_entry = ttk.Entry(input_frame)
        self.vol_entry.grid(row=0, column=1)
        
        ttk.Label(input_frame, text="Weight (kg):").grid(row=1, column=0)
        self.weight_entry = ttk.Entry(input_frame)
        self.weight_entry.grid(row=1, column=1)
        
        ttk.Button(input_frame, text="Add Item", command=self.add_item).grid(row=2, columnspan=2, pady=5)
        
        # Container Limits
        ttk.Label(input_frame, text="Max Volume (m³):").grid(row=3, column=0)
        ttk.Entry(input_frame, textvariable=self.max_volume).grid(row=3, column=1)
        
        ttk.Label(input_frame, text="Max Weight (kg):").grid(row=4, column=0)
        ttk.Entry(input_frame, textvariable=self.max_weight).grid(row=4, column=1)
        
        ttk.Button(input_frame, text="Pack Items", command=self.pack_items).grid(row=5, columnspan=2, pady=5)
    
    def setup_results_frame(self):
        results_frame = ttk.LabelFrame(self.root, text="Packing Results", padding=10)
        results_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        
        # Notebook for Bins and Items
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Bins Summary Tab
        self.summary_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_tab, text="Containers Summary")
        
        self.tree = ttk.Treeview(self.summary_tab, columns=("Volume", "Weight"), show="headings")
        self.tree.heading("Volume", text="Volume Used (m³)")
        self.tree.heading("Weight", text="Weight Used (kg)")
        self.tree.pack(fill="both", expand=True)
        
        # Export Button
        ttk.Button(results_frame, text="Export to CSV", command=self.export_csv).pack(pady=5)
    
    def add_item(self):
        try:
            volume = float(self.vol_entry.get())
            weight = float(self.weight_entry.get())
            self.items.append((volume, weight))
            messagebox.showinfo("Success", f"Added item: {volume}m³, {weight}kg")
            self.vol_entry.delete(0, tk.END)
            self.weight_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Use numbers only.")
    
    def pack_items(self):
        if not self.items:
            messagebox.showerror("Error", "No items to pack!")
            return
        
        self.bins = []
        items_sorted = sorted(self.items, key=lambda x: (-x[0], -x[1]))  # Sort by volume then weight
        

        #algorithm use(first fit decreasing)
        
        for item in items_sorted:
            vol, weight = item
            placed = False
            
            for bin in self.bins:
                bin_vol = sum(b[0] for b in bin) # Total volume in current bin
                bin_weight = sum(b[1] for b in bin) # Total weight in current bin
                
                if (bin_vol + vol <= self.max_volume.get() and 
                    bin_weight + weight <= self.max_weight.get()):
                    bin.append(item)     # Add to existing bin
                    placed = True
                    break
            
            if not placed:
                self.bins.append([item])  # Create new bin
        
        self.display_results()
    
    def display_results(self):
        # Clear previous results
        self.tree.delete(*self.tree.get_children())
        for tab in self.notebook.tabs()[1:]:  # Remove old item tabs
            self.notebook.forget(tab)
        
        # Update summary
        for i, bin in enumerate(self.bins, 1):
            total_vol = sum(b[0] for b in bin)
            total_weight = sum(b[1] for b in bin)
            self.tree.insert("", "end", values=(
                f"{total_vol:.2f}/{self.max_volume.get()}",
                f"{total_weight:.2f}/{self.max_weight.get()}"
            ))
            
            # Create a tab for each container's items
            container_tab = ttk.Frame(self.notebook)
            self.notebook.add(container_tab, text=f"Container {i}")
            
            # Treeview for items in this container
            item_tree = ttk.Treeview(container_tab, columns=("Volume", "Weight"), show="headings")
            item_tree.heading("Volume", text="Volume (m³)")
            item_tree.heading("Weight", text="Weight (kg)")
            item_tree.pack(fill="both", expand=True)
            
            for item in bin:
                item_tree.insert("", "end", values=(f"{item[0]:.2f}", f"{item[1]:.2f}"))
        
        efficiency = sum(b[0] for b in self.items) / (len(self.bins) * self.max_volume.get())
        messagebox.showinfo("Packing Complete", 
                          f"Used {len(self.bins)} containers\nEfficiency: {efficiency:.1%}")
    
    def export_csv(self):
        if not self.bins:
            messagebox.showerror("Error", "No results to export!")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:
            with open(file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Container", "Item Volume (m³)", "Item Weight (kg)", "Total Volume", "Total Weight"])
                for i, bin in enumerate(self.bins, 1):
                    for item in bin:
                        writer.writerow([f"Container {i}", item[0], item[1]])
                    writer.writerow(["TOTAL", "", "", sum(b[0] for b in bin), sum(b[1] for b in bin)])
                    writer.writerow([])  # Empty row between containers
            messagebox.showinfo("Success", "Results exported to CSV!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BinPackingGUI(root)
    root.mainloop()