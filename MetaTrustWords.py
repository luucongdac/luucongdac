import tkinter as tk
from tkinter import messagebox, scrolledtext
import time

# ===============================
# CORE
# ===============================

MetaTrustWords_encoded = "nenomFaggegsernvuroOUiptteSeulnaGxduWyrWnNldaugYbBTlYsratPlfrsrMbfesblpyfrsividiVTtacctmnntelyrRmMnpalPinaWBtepneJlmaacueReddeFKalaazGreenobtmpbTsscenOpterbnernBlueeiceuenhclarretCrIlPoaetaaoebaesyddisgosoXhrbm"

def random_upper(seed):
    seed = next_seed(seed)
    letter = chr((seed % 26) + 65)
    return letter, seed

def random_int(seed):
    return (seed * 1103515245 + 12345) % (2**31)

def password_to_seed(password):
    seed = 0
    i = 0
    while i < len(password):
        seed = (seed * 257 + ord(password[i])) % (2**512)
        i += 1

    # stretching nhưng luôn giữ 512-bit
    i = 0
    minutes_to_generate = 0.1 #minutes
    while i < 1399000 * 60 * minutes_to_generate:  #---> càng to càng lâu để tính ra
        seed = (seed * 6364136223846793005 + 1442695040888963407) % (2**512)
        i += 1

    return seed


def next_seed(seed):
    return (seed * 6364136223846793005 + 1442695040888963407) % (2**512)

def generate_permutation(n, seed):
    perm = []
    i = 0
    while i < n:
        perm.append(i)
        i += 1

    i = n - 1
    while i > 0:
        seed = next_seed(seed)
        j = seed % (i + 1)

        tmp = perm[i]
        perm[i] = perm[j]
        perm[j] = tmp

        i -= 1

    return perm

#chèn ký tự đặc biệt

def insert_random_string(base_string, insert_items):
    items = [i.strip() for i in insert_items.split(",") if i.strip()]
    n = len(items)

    # kiểm tra trùng
    for item in items:
        if item in base_string:
            print(f"Lỗi: '{item}' đã tồn tại trong chuỗi gốc")
            exit()

    length = len(base_string)
    seed = length + n

    # tạo vị trí chèn không trùng trên string gốc
    positions = set()
    while len(positions) < n:
        seed = random_int(seed)
        pos = seed % (length + 1)
        positions.add(pos)

    positions = sorted(positions)

    # cắt chuỗi theo vị trí
    result_parts = []
    last = 0

    for pos, item in zip(positions, items):
        result_parts.append(base_string[last:pos])
        result_parts.append(item)
        last = pos

    result_parts.append(base_string[last:])

    return "".join(result_parts)

def de_insert(modified_string, insert_items):
    items = [i.strip() for i in insert_items.split(",") if i.strip()]

    result = modified_string

    for item in items:
        count = result.count(item)

        if count == 0:
            print(f"Lỗi: không tìm thấy '{item}' trong chuỗi")
            exit()

        if count > 1:
            print(f"Lỗi: '{item}' xuất hiện nhiều lần → không thể khôi phục chính xác")
            exit()

        result = result.replace(item, "", 1)

    return result
# ===============================
# ENCODE
# ===============================

def encode(password, words):
    seed_main = password_to_seed(password)

    seed_sep  = (seed_main + 1234567) % 2147483647
    seed_perm = (seed_main + 7654321) % 2147483647

    original = ""
    i = 0

    while i < len(words):
        original = original + words[i]

        if i != len(words) - 1:
            sep, seed_sep = random_upper(seed_sep)
            original = original + sep

        i = i + 1

    perm = generate_permutation(len(original), seed_perm)

    encoded = [""] * len(original)

    i = 0
    while i < len(original):
        encoded[i] = original[perm[i]]
        i = i + 1

    return "".join(encoded)


# ===============================
# DECODE
# ===============================

def get_or_words(encoded_string, password):
    seed_main = password_to_seed(password)

    seed_perm = (seed_main + 7654321) % 2147483647

    perm = generate_permutation(len(encoded_string), seed_perm)

    decoded = [""] * len(encoded_string)

    i = 0
    while i < len(encoded_string):
        decoded[perm[i]] = encoded_string[i]
        i = i + 1

    joined = "".join(decoded)

    words = []
    current = ""

    i = 0
    while i < len(joined):
        ch = joined[i]

        if ch >= 'A' and ch <= 'Z':
            if current != "":
                words.append(current)
                current = ""
        else:
            current = current + ch

        i = i + 1

    if current != "":
        words.append(current)

    return words


# ================= GUI =================

def get_inputs():
    password = entry_password.get()
    passkey = entry_passkey.get()
    denied = entry_denied.get()
    encoded = entry_encoded.get()
    raw_words = text_secret.get("1.0", tk.END).strip()

    if "," in raw_words:
        words = [w.strip() for w in raw_words.split(",") if w.strip()]
    else:
        words = [w.strip() for w in raw_words.splitlines() if w.strip()]

    return password, passkey, denied, encoded, words


def do_encode():
    try:
        start_encode = time.perf_counter()
        password, passkey, denied_words, encoded_gui, secret_words = get_inputs()

        encoded = encode(password + passkey, secret_words)
        encoded_with_insert = insert_random_string(encoded, denied_words)
        de_insert_encoded_with_insert  = de_insert(encoded_with_insert, denied_words)
        end_encode = time.perf_counter()
        encode_time = end_encode - start_encode

        result_box.delete("1.0", tk.END)

        # result_box.insert(tk.END, f"ENCODED:  {encoded} \n")
        result_box.insert(tk.END, f'-> ENCODED with inserted: \n\t"{encoded_with_insert}"\n')
        # result_box.insert(tk.END, f"de_inserted with ENCODED with inserted: {de_insert_encoded_with_insert}\n")
        result_box.insert(tk.END, f"     --> the same before and after insert-deInsert: {encoded==de_insert_encoded_with_insert}\n")
        result_box.insert(tk.END, f"->ENCODE TIME: {encode_time:.6f} seconds")
        entry_encoded.delete(0,tk.END)
        entry_encoded.insert(0, encoded_with_insert)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def do_decode():
    try:
        password, passkey, denied_words, encoded_gui, secret_words = get_inputs()
        start_decode = time.perf_counter()
        decoded_words = get_or_words(de_insert(encoded_gui, denied_words), password + passkey)
        end_decode = time.perf_counter()
        decode_time = end_decode - start_decode

        text_secret.delete("1.0", tk.END)
        for i in range(0,len(decoded_words)):
            text_secret.insert(tk.END,f"{i}\t{decoded_words[i]}\n" )

        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, f"\n->DECODED: {len(decoded_words)} words \n --> \n {decoded_words}\n")
        result_box.insert(tk.END, f"->DECODE TIME: {decode_time:.6f} seconds")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ================= WINDOW =================
FONT = ("Segoe UI", 20)
FONT_BIG = ("Segoe UI", 30, "bold")

BG_MAIN = "#0d1117"        # nền chính (đen xám)
BG_PANEL = "#161b22"       # nền panel
TEXT_COLOR = "#e6edf3"     # chữ trắng dịu
ACCENT = "#00FFD1"         # xanh neon
ENTRY_BG = "#0b0f14"       # nền ô nhập
RESULT_GREEN = "#00FF88"   # màu kết quả

root = tk.Tk()
root.title("MetaTrust Words")
root.geometry("1600x900")
root.configure(bg=BG_MAIN)

main_frame = tk.Frame(root, bg=BG_MAIN)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# LEFT SIDE
left = tk.Frame(main_frame, bg=BG_PANEL)
left.pack(side="left", fill="both", expand=True, padx=(0,10))

# RIGHT SIDE
right = tk.Frame(main_frame, bg=BG_PANEL)
right.pack(side="right", fill="both")

tk.Label(left, text="MetaTrust Words Tool",
         font=FONT_BIG, fg=ACCENT, bg=BG_PANEL).pack(pady=10)

def styled_label(parent, text):
    return tk.Label(parent, text=text, font=FONT,
                    fg=TEXT_COLOR, bg=BG_PANEL)

def styled_entry(parent):
    return tk.Entry(parent, font=FONT, fg=ACCENT,
                    bg=ENTRY_BG, insertbackground=ACCENT,
                    relief="flat")

styled_label(left, "\t\tPassword").pack(anchor="w")
entry_password = styled_entry(left)
entry_password.pack(fill="x")
entry_password.insert(0, "Ab#c@123^XyZ7*89!Q")

styled_label(left, "\t\tPasskey").pack(anchor="w")
entry_passkey = styled_entry(left)
entry_passkey.pack(fill="x")
entry_passkey.insert(0, "1234")

styled_label(left, "\t\tDenied Words").pack(anchor="w")
entry_denied = styled_entry(left)
entry_denied.pack(fill="x")
entry_denied.insert(0, "Red,Green,Blue")

styled_label(left, "\t\tEncoded String").pack(anchor="w")
entry_encoded = styled_entry(left)
entry_encoded.pack(fill="x")
entry_encoded.insert(0, MetaTrustWords_encoded)

# BUTTONS
btn_frame = tk.Frame(left, bg=BG_PANEL)
btn_frame.pack(pady=15)

def styled_button(parent, text, cmd):
    return tk.Button(parent,
                     text=text,
                     font=FONT_BIG,
                     bg="#21262d",
                     fg=ACCENT,
                     activebackground="#30363d",
                     activeforeground=ACCENT,
                     relief="flat",
                     command=cmd,
                     padx=15,
                     pady=8)

styled_button(btn_frame, "ENCODE", do_encode).grid(row=0, column=0, padx=10)
styled_button(btn_frame, "DECODE", do_decode).grid(row=0, column=1, padx=10)

styled_label(left, "Result").pack(anchor="w", pady=(10,0))

result_box = scrolledtext.ScrolledText(
    left,
    height=10,
    font=FONT,
    fg=RESULT_GREEN,
    bg=ENTRY_BG,
    insertbackground=RESULT_GREEN,
    relief="flat"
)
result_box.pack(fill="both", expand=True)

# RIGHT PANEL
tk.Label(right, text="Secret Words",
         font=FONT_BIG, fg=ACCENT, bg=BG_PANEL).pack(pady=10)

text_secret = scrolledtext.ScrolledText(
    right,
    width=30,
    height=30,
    font=FONT,
    fg=TEXT_COLOR,
    bg=ENTRY_BG,
    insertbackground=ACCENT,
    relief="flat"
)
text_secret.pack(fill="both", expand=True)

default_words = """begin
sudden
fabric
peanut
crane
unfold
clump
number
insert
galaxy
home
barrel
season
vintage
rally
inform
gravity
end
protect
brass
tab
comic
supply
delete
slogan
sample
earth
enter
blast
zebra
end"""

text_secret.insert(tk.END, default_words)

root.mainloop()
