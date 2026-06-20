# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open(r'D:\桌面\abc\extracted_text.txt', 'r', encoding='utf-8') as f:
    full_text = f.read()

# Find all section contents
import re
sections = full_text.split('\x0c')

# Extract key content from each section
def get_section_text(text, start_marker, end_marker=None):
    start = text.find(start_marker)
    if start == -1:
        return ''
    if end_marker:
        end = text.find(end_marker, start + len(start_marker))
        if end == -1:
            return text[start:].strip()
        return text[start:end].strip()
    return text[start:].strip()

# Extract abstract
abstract = ''
for s in sections:
    if '摘 要' in s:
        abstract = s
        break

# Extract ch1 intro
ch1 = ''
for s in sections:
    if '第一章 绪论' in s or '1.1 研究背景' in s:
        ch1 = s
        break

# Extract ch2
ch2 = ''
for s in sections:
    if '第二章 实验材料与方法' in s or '2.1 实验材料制备' in s:
        ch2 = s
        break

# Extract ch3
ch3 = ''
for s in sections:
    if '第三章 结果与讨论' in s or '3.1 不同温度' in s:
        ch3 = s
        break

# Extract ch4
ch4 = ''
for s in sections:
    if '第四章 结论与展望' in s or '4.1 主要研究结论' in s:
        ch4 = s
        break

print('=== ABSTRACT ===')
print(abstract[:1000])
print()
print('=== CHAPTER 1 ===')
print(ch1[:1000])
print()
print('=== CHAPTER 2 ===')
print(ch2[:1500])
print()
print('=== CHAPTER 3 ===')
print(ch3[:1500])
print()
print('=== CHAPTER 4 ===')
print(ch4[:1500])
