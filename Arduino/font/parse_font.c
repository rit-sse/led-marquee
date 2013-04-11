
<!-- saved from url=(0046)http://heim.ifi.uio.no/haakoh/avr/parse_font.c -->
<html><head><meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1"><style type="text/css"></style></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">#include &lt;stdio.h&gt;
#include &lt;stdlib.h&gt;

int main()
{
  char *line;
  int y;
  int i;
  int j;
  char *s;
  unsigned char chars[256][5];
  int nchars;
  line = malloc(1000);

  /* Read standard in */
  nchars = 0;
  while (1)
  {
    /* Read next char */
    chars[nchars][0] = 0;
    chars[nchars][1] = 0;
    chars[nchars][2] = 0;
    chars[nchars][3] = 0;
    chars[nchars][4] = 0;
    for (y=6; y&gt;=0; y--)
    {
      s = fgets(line, 1000, stdin);
      if (s != line) goto nomorechars;
      for (i=0; line[i] != 0 &amp;&amp; i &lt; 5; i++)
        if (line[i] == '*')
          chars[nchars][i] |= 1&lt;&lt;y;
    }
    nchars++;
    s = fgets(line, 1000, stdin);
    if (s != line) goto nomorechars;
  }

nomorechars:

  /* Write fonts to standard out */
  printf("const int font_count = %d;\n", nchars);
  printf("const unsigned char font[%d][5] = {", nchars);
  for (i=0; i&lt;nchars; i++)
  {
    printf("\n  {");
    for (j=0; j&lt;5; j++)
    {
      printf("0x%02x%s", chars[i][j], (j&lt;4)?", ":"");
    }
    printf("}%s", (i&lt;nchars-1)?",":"");
  }
  printf("};\n");
  
  return 0;
}
</pre></body></html>