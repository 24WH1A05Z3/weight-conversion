import tkinter as tk
from tkinter import ttk, messagebox
import math

class EnhancedWeightConverter:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        self.create_variables()
        self.create_widgets()
        self.setup_bindings()
        
    def setup_window(self):
        """Configure main window properties"""
        self.master.title("Enhanced Weight Converter")
        self.master.geometry("600x500")
        self.master.configure(bg='#f0f0f0')
        self.master.resizable(True, True)
        
        # Center window on screen
        self.master.update_idletasks()
        x = (self.master.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.master.winfo_screenheight() // 2) - (500 // 2)
        self.master.geometry(f"600x500+{x}+{y}")
        
    def create_variables(self):
        """Initialize all tkinter variables"""
        self.weight_var = tk.StringVar()
        self.from_unit_var = tk.StringVar(value="kg")
        self.to_unit_var = tk.StringVar(value="lbs")
        self.result_var = tk.StringVar(value="Enter weight to convert")
        
        # Available units with full names
        self.units = {
            "kg": "Kilograms",
            "lbs": "Pounds", 
            "g": "Grams",
            "oz": "Ounces",
            "stone": "Stones",
            "ton": "Metric Tons"
        }
        
        # Conversion factors to kilograms
        self.to_kg_factors = {
            "kg": 1.0,
            "lbs": 0.453592,
            "g": 0.001,
            "oz": 0.0283495,
            "stone": 6.35029,
            "ton": 1000.0
        }
        
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main container with padding
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Weight Converter", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Conversion Input", padding="15")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Weight input
        ttk.Label(input_frame, text="Weight:", font=("Arial", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        
        self.weight_entry = ttk.Entry(input_frame, textvariable=self.weight_var, 
                                     font=("Arial", 11), width=15)
        self.weight_entry.grid(row=0, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        self.weight_entry.focus()
        
        # From unit
        ttk.Label(input_frame, text="From:", font=("Arial", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        
        self.from_combo = ttk.Combobox(input_frame, textvariable=self.from_unit_var,
                                      values=list(self.units.keys()), 
                                      state="readonly", width=12)
        self.from_combo.grid(row=1, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # To unit
        ttk.Label(input_frame, text="To:", font=("Arial", 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        
        self.to_combo = ttk.Combobox(input_frame, textvariable=self.to_unit_var,
                                    values=list(self.units.keys()), 
                                    state="readonly", width=12)
        self.to_combo.grid(row=2, column=1, padx=(10, 0), pady=5, sticky=tk.W)
        
        # Swap button
        swap_btn = ttk.Button(input_frame, text="⇄ Swap", command=self.swap_units, width=8)
        swap_btn.grid(row=1, column=2, rowspan=2, padx=(20, 0), pady=5)
        
        # Convert button
        convert_btn = ttk.Button(input_frame, text="Convert", command=self.convert_weight,
                                style="Accent.TButton")
        convert_btn.grid(row=3, column=0, columnspan=3, pady=(15, 5))
        
        # Result section
        result_frame = ttk.LabelFrame(main_frame, text="Result", padding="15")
        result_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.result_label = ttk.Label(result_frame, textvariable=self.result_var,
                                     font=("Arial", 12, "bold"), foreground="blue")
        self.result_label.pack()
        
        # Quick conversion section
        quick_frame = ttk.LabelFrame(main_frame, text="Quick Reference", padding="15")
        quick_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable text widget for quick conversions
        text_frame = ttk.Frame(quick_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.quick_text = tk.Text(text_frame, height=8, width=50, font=("Courier", 9),
                                 state=tk.DISABLED, bg="#f8f8f8")
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.quick_text.yview)
        self.quick_text.configure(yscrollcommand=scrollbar.set)
        
        self.quick_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.update_quick_reference()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        
    def setup_bindings(self):
        """Setup event bindings"""
        self.weight_entry.bind('<Return>', lambda e: self.convert_weight())
        self.weight_entry.bind('<KeyRelease>', self.on_input_change)
        self.from_combo.bind('<<ComboboxSelected>>', self.on_unit_change)
        self.to_combo.bind('<<ComboboxSelected>>', self.on_unit_change)
        
    def convert_weight(self):
        """Perform weight conversion"""
        try:
            weight_str = self.weight_var.get().strip()
            if not weight_str:
                self.result_var.set("Please enter a weight value")
                return
                
            weight = float(weight_str)
            if weight < 0:
                self.result_var.set("Weight cannot be negative")
                return
                
            from_unit = self.from_unit_var.get()
            to_unit = self.to_unit_var.get()
            
            if from_unit == to_unit:
                self.result_var.set(f"{weight} {self.units[from_unit]}")
                self.status_var.set("Same unit conversion")
                return
            
            # Convert to kg first, then to target unit
            weight_in_kg = weight * self.to_kg_factors[from_unit]
            converted_weight = weight_in_kg / self.to_kg_factors[to_unit]
            
            # Format result nicely
            if converted_weight >= 1000:
                result = f"{converted_weight:,.2f}"
            elif converted_weight >= 1:
                result = f"{converted_weight:.3f}"
            else:
                result = f"{converted_weight:.6f}".rstrip('0').rstrip('.')
            
            self.result_var.set(f"{result} {self.units[to_unit]}")
            self.status_var.set(f"Converted {weight} {from_unit} to {to_unit}")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
            self.result_var.set("Invalid input")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion error: {str(e)}")
            
    def swap_units(self):
        """Swap from and to units"""
        from_unit = self.from_unit_var.get()
        to_unit = self.to_unit_var.get()
        self.from_unit_var.set(to_unit)
        self.to_unit_var.set(from_unit)
        if self.weight_var.get().strip():
            self.convert_weight()
        self.status_var.set("Units swapped")
        
    def on_input_change(self, event=None):
        """Handle input changes for live conversion"""
        if self.weight_var.get().strip():
            self.convert_weight()
            
    def on_unit_change(self, event=None):
        """Handle unit selection changes"""
        if self.weight_var.get().strip():
            self.convert_weight()
        self.update_quick_reference()
        
    def update_quick_reference(self):
        """Update quick reference conversions"""
        from_unit = self.from_unit_var.get()
        
        self.quick_text.config(state=tk.NORMAL)
        self.quick_text.delete(1.0, tk.END)
        
        header = f"1 {self.units[from_unit]} equals:\n"
        self.quick_text.insert(tk.END, header, "header")
        self.quick_text.insert(tk.END, "-" * 30 + "\n")
        
        for unit, name in self.units.items():
            if unit != from_unit:
                # Convert 1 unit of from_unit to target unit
                weight_in_kg = 1.0 * self.to_kg_factors[from_unit]
                converted = weight_in_kg / self.to_kg_factors[unit]
                
                if converted >= 1000:
                    value = f"{converted:,.3f}"
                elif converted >= 1:
                    value = f"{converted:.4f}"
                else:
                    value = f"{converted:.6f}".rstrip('0').rstrip('.')
                
                line = f"{value:>12} {name}\n"
                self.quick_text.insert(tk.END, line)
        
        self.quick_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = EnhancedWeightConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()