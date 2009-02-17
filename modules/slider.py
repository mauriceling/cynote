def slider(data, start, end = None):
    if end == None or end > len(data): end = len(data) - start
    rawdata = [data[index:index+window]
               for index in range(len(data))
                   for window in range(start, end)
                       if index+window <= len(data)]
    return [x for x in rawdata
            if len(x) > start]

#t = "Meanwhile, let me know if you need clarification about the claiming process or matters regarding ASP / SMP anytime."
#for i in slide(t,10,20): print i
