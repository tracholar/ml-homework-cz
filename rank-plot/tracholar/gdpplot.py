#coding:utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



def animate_show(file, name_col, year_range, topn=10, sep='\t',
                 interval=500):
    df = pd.read_csv(file, sep=sep)
    fig = plt.figure(figsize=(10, 6))

    barcollection = plt.barh(range(0,topn), [10]*topn)
    ax = fig.gca()

    texts = []
    def update_function(year):
        x = df[name_col]
        y = df[str(year)]
        data = filter(lambda z: not np.isnan(z[1]), zip(x, y))
        print data
        data.sort(key=lambda z:z[1])
        x, y = zip(*data[-topn:])

        max_width = max(y)*1.2
        ax.set_xlim([0, max_width])
        ax.set_yticklabels([])

        #print data[:10]
        for txt in texts:
            txt.remove()
        del texts[:]

        for i, b in enumerate(barcollection.patches):
            b.set_width(y[i])
            yoffset = b.get_y()
            texts.append( ax.text(max_width*0.9, yoffset, u'{0:.0f}亿'.format(y[i]/1e8)) )
            texts.append( ax.text(max_width*0.01, yoffset, x[i]) )

        texts.append(ax.text(max_width*0.7, 0.3, u'{}年'.format(year), fontsize=25))






    ani = animation.FuncAnimation(fig, update_function, year_range,
                                  interval=interval, repeat=False , blit=False)


    plt.show()


if __name__ == '__main__':
    animate_show('data.txt', 'Country Name', np.arange(1960, 2019), topn=20)