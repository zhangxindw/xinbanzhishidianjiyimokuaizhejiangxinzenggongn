# -*- coding: utf-8 -*-
import struct, os, glob
from olefile import OleFileIO

candidates = list(glob.glob(r'D:\桌面\杂务\水利水电\毕业设计\毕业设计上交\*.doc'))
print("Found files:", candidates)
if candidates:
    DOC_PATH = candidates[0]
    ole = OleFileIO(DOC_PATH)
    word_doc = ole.openstream('WordDocument').read()
    print("WordDocument size:", len(word_doc))
    
    with open(DOC_PATH, 'rb') as f:
        raw = f.read()
    
    results = []
    chars = []
    for i in range(0, len(raw) - 1, 2):
        try:
            c = raw[i:i+2].decode('utf-16-le')
            if c.isprintable() or c in '\n\r\t':
                chars.append(c)
            else:
                if len(chars) > 10:
                    piece = ''.join(chars)
                    if any('\u4e00' <= ch <= '\u9fff' or '\u3000' <= ch <= '\u303f' for ch in piece):
                        results.append(piece)
                chars = []
        except:
            if len(chars) > 10:
                piece = ''.join(chars)
                if any('\u4e00' <= ch <= '\u9fff' or '\u3000' <= ch <= '\u303f' for ch in piece):
                    results.append(piece)
            chars = []
    
    if len(chars) > 10:
        piece = ''.join(chars)
        if any('\u4e00' <= ch <= '\u9fff' or '\u3000' <= ch <= '\u303f' for ch in piece):
            results.append(piece)
    
    long_chunks = [c for c in results if len(c) > 30]
    for i, chunk in enumerate(long_chunks[:15]):
        print(f'Chunk {i} ({len(chunk)} chars):', chunk[:150])
    
    output = '\n'.join(long_chunks)
    outpath = 'D:/桌面/abc/extracted_text.txt'
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f'Total: {len(output)} chars, {len(long_chunks)} chunks')
    print(f'Saved to: {outpath}')
    ole.close()
