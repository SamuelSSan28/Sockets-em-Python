import mechanize

br = mechanize.Browser()
br.set_handle_robots( False )
br.addheaders = [('User-agent', 'Firefox')]

url = "https://login.ufpi.br:6082/php/uid.php?vsys=1&rule=0&url=http://conecta.ufpi.br%2f"

br.open(url)

br.select_form( nr = 0 )
br.form[ 'user' ] = 'samuelssan28'
br.form[ 'passwd' ] = 'sam28muel'
br.submit()