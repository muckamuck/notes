html = '''<html>
  <head>
    <style>
a {
        text-decoration: none;
                display: inline-block;
                        padding: 8px 16px;
}

a:hover {
        background-color: #ddd;
                color: black;
}

.previous {
        background-color: #4CAF50;
                color: white;
}

.next {
        background-color: #4CAF50;
                color: white;
}

.round {
        border-radius: 50%;
}

    </style>
  </head>
  <body style="background-color: #5e5e5e;">
    <p style="text-align: center;">
    <a href="${nextHtml}"><img src="${smallImage}" /></a>
    <br/>
    <a href="${prevHtml}" class="previous round"><strong>&#8249;</strong></a>
    <a href="${nextHtml}" class="next round"><strong>&#8250;</strong></a>
    <br/>
    <br/>
    <br/>
    <a href="${bigImage}"
        class="next round"
        download="${stub}"
        alt="Download"><strong>&#8675;</strong></a>
    </p>
  </body>
</html>
'''
