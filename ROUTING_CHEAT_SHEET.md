# Streamlit Multi-Page Routing Cheat Sheet

## The Golden Rule

```
File Name (Physical)    Display Name (Routing)
────────────────────────────────────────────
00_home.py        →     "pages/home.py"
01_book_tickets.py →    "pages/book_tickets.py"
02_my_bookings.py  →    "pages/my_bookings.py"
03_login.py        →    "pages/login.py"
```

**Numeric prefix is ONLY for sidebar ordering. Remove it when routing.**

## Quick Fix Template

### ❌ BEFORE (NOT_FOUND Error)
```python
if st.button("Go to Booking"):
    st.switch_page("pages/01_book_tickets.py")  # ← WRONG!
```

### ✅ AFTER (Working)
```python
if st.button("Go to Booking"):
    st.switch_page("pages/book_tickets.py")  # ← RIGHT!
```

## Common Patterns to Fix

| Pattern | Wrong ❌ | Right ✅ |
|---------|---------|---------|
| Direct navigation | `pages/00_home.py` | `pages/home.py` |
| Sidebar links | `pages/01_booking.py` | `pages/booking.py` |
| Login redirect | `pages/02_profile.py` | `pages/profile.py` |
| Dynamic routing | `pages/03_login.py` | `pages/login.py` |

## How to Check Your Code

```bash
# Search for this pattern (indicates problem)
grep -r 'st.switch_page.*[0-9][0-9]_' frontend/

# Should find nothing if your code is correct
```

## Why It Works This Way

Streamlit separates **display** (file names) from **routing** (page references) to:

1. ✅ Allow reordering pages without breaking code
2. ✅ Keep code clean and decoupled from presentation
3. ✅ Support dynamic page ordering
4. ✅ Prevent path traversal security issues

## Test Your Fix

```bash
# 1. Start the app
python -m streamlit run frontend/app.py

# 2. Test each button that navigates
# Should see smooth transitions, NO ERROR messages

# 3. Check terminal
# Should see: "You can now view your Streamlit app"
# Should NOT see: "NOT_FOUND" or "ERROR"
```

## Remember

> **File names organize the sidebar. Page references navigate the app.**
> Never confuse the two!

