html = """
<rich-text-document>
<p>
  <a href="https://springload.github.io/draftail/">Draftail</a>
  works well with
  <a href="https://github.com/springload/draftjs_exporter">draftjs_exporter</a>!
</p>
<img alt="Test image alt text" src="https://placekitten.com/g/260/160"/>
<ul>
  <li>
    List item
    <ul>
     <li><em>Nested</em></li>
    </ul>
  </li>
  <li>
    and back
  </li>
</ul></rich-text-document>
"""

from html2contentstate import convert

print(repr(convert(html)))
