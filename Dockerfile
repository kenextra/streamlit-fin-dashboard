FROM python:3.8

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

RUN wget -O ta-lib-0.4.0-src.tar.gz http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    wget -O TA-Lib-0.4.19.tar.gz https://files.pythonhosted.org/packages/ac/cf/681911aa31e04ba171ab4d523a412f4a746e30d3eacb1738799d181e028b/TA-Lib-0.4.19.tar.gz && \
    tar xvf TA-Lib-0.4.19.tar.gz && \
    cd TA-Lib-0.4.19 && \
    python3 setup.py install && \
    cd ..

RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz TA-Lib-0.4.19.tar.gz TA-Lib-0.4.19

EXPOSE 8080

COPY . /app

CMD streamlit run --server.port 8080 --server.enableCORS false app.py