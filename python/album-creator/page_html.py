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
  <body>


<p style="text-align: center;">
<a href="${nextHtml}"><img src="${smallImage}" /></a>
<br/>
<a href="${prevHtml}" class="previous round">&#8249;</a>
<a href="${nextHtml}" class="next round">&#8250;</a>
<br/>
<br/>
<br/>
<a href="${bigImage}" target="xldl3884">Download</a>
</p>

  </body>
</html>
'''
