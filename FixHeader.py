source = "<?xml version='1.0' encoding='UTF-8'?><svg id='b' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 128 128'><defs><style>.c{fill:none;stroke:currentColor;stroke-linecap:round;stroke-linejoin:round;stroke-width:2.126px;}</style></defs><line class='c' x1='66.5106' y1='46.8446' x2='66.5106' y2='86.4616'/><line class='c' x1='46.7021' y1='66.6531' x2='86.3191' y2='66.6531'/><rect class='c' x='72.1371' y='78.499' width='40.7739' height='26.3831' rx='6.6456' ry='6.6456' transform='translate(38.1152 -26.6629) rotate(20.5703)'/><path class='c' d='M82.2833,96.1533c-1.2014-2.6449-1.3959-5.7425-.2945-8.6772s3.2858-5.1396,5.9306-6.341'/><path class='c' d='M102.9377,86.7711c1.2014,2.6449,1.3959,5.7425.2945,8.6772s-3.2858,5.1396-5.9306,6.341'/><path class='c' d='M86.6098,94.188c-.7035-1.5385-.8128-3.3424-.1745-5.0432s1.9074-2.9874,3.4494-3.6832'/><path class='c' d='M98.6111,88.7364c.6979,1.5365.8128,3.3424.1745,5.0432s-1.9129,2.9852-3.4494,3.6832'/><path class='c' d='M90.9288,92.2261c-.1924-.4336-.2263-.9346-.0469-1.4126s.5345-.833.9647-1.033'/><path class='c' d='M94.2922,90.6983c.1924.4336.2263.9346.0469,1.4126s-.5345.833-.9647,1.033'/><circle class='c' cx='40.4148' cy='35.8194' r='7.1713'/><path class='c' d='M52.5446,51.8322c-.0515-3.7062-1.7796-7.0016-4.4482-9.1911-1.8347,2.2039-4.5964,3.6102-7.6813,3.6102s-5.8468-1.4063-7.6817-3.6101c-2.6686,2.1921-4.3935,5.4843-4.4449,9.1909'/><rect class='c' x='20.6027' y='21.4084' width='39.6313' height='39.6313'/><rect class='c' x='26.9665' y='22.7319' width='26.9036' height='32.2908' transform='translate(79.2957 -1.541) rotate(90)'/></svg>"

def fixHeader(svgcontent):
    
    firstIndexOfDefsStyle = ""
    lastIndexOfDefsStyle = ""
    strokeWidth = ""
    strokeLineJoin = ""
    strokeLineCaps = ""
    stroke = ""
    fill = ""
    fillRule = ""
    numberOfClasses = ""

    if "<defs><style>." in svgcontent:
        firstIndexOfDefsStyle = svgcontent.index("<defs><style>.")
        lastIndexOfDefsStyle = svgcontent.index("</style></defs>")
        
        styles = svgcontent[firstIndexOfDefsStyle:lastIndexOfDefsStyle]

        ## h több mint 1 class van benne, akkor nem csinálunk semmit.
        numberOfClasses = styles.count('{')
        if numberOfClasses > 1:
            print("More than one classes. Skipping...")
            return False
        
        if "stroke-width:" in styles:
            strokeWidth = returnClassValue(styles,"stroke-width")
        if "stroke-linecap:" in styles:
            strokeLineCaps = returnClassValue(styles,"stroke-linecap")
        if "stroke-linejoin:" in styles:
            strokeLineJoin = returnClassValue(styles,"stroke-linejoin")
        if "stroke:" in styles:
            stroke = returnClassValue(styles,"stroke")
        if "fill:" in styles:
            fill = returnClassValue(styles, "fill")
        if "fill-rule:" in styles:
            fillRule = returnClassValue(styles, "fill-rule")

        ## clear styles
        source = svgcontent[:firstIndexOfDefsStyle]
        source += svgcontent[lastIndexOfDefsStyle+len("</style></defs>"):]

        ## Add to header
        headerAddition = f" stroke=\"{stroke}\" stroke-width=\"{strokeWidth}\" stroke-linecap=\"{strokeLineCaps}\" stroke-linejoin=\"{strokeLineJoin}\" fill=\"{fill}\" fill-rule=\"{fillRule}\" "
        fixFrom = source.index(">",source.index("<svg"))
        firsthalf = source[:fixFrom]
        lasthalf = source[fixFrom:]
        done = firsthalf + headerAddition + lasthalf
        return done
    else:
        return False

def returnClassValue(source,param):
    cursor = source.index(f"{param}:")
    valueStart = source.index(":",cursor)
    cursor = valueStart
    valueEnd = source.index(";",cursor)
    value = source[valueStart+1:valueEnd]
    return value


print(fixHeader(source))
