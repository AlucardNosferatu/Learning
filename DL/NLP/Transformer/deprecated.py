def add_sta_and_end_cn(region, mss=20):
    region.insert(0, '<STA>')
    region.append('<END>')
    if len(region) > mss:
        return None
    else:
        while len(region) < mss:
            region.append('<PAD>')
        return region
