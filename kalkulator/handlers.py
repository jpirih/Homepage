from site_handlers import BaseHandler

# Kontroler za kalkulator
class KalkulatorHandler(BaseHandler):
    def get(self):
        return self.render_template("kalkulator.html")

    def post(self):
        err_msg = "Obvezen je vnos stevil in operacije \n Pazi pa Deljenje z 0 ni dovoljeno"
        params = {"deljenje_err":err_msg}
        try:
            num1 = float(self.request.get("stevilo1"))
            num2 = float(self.request.get("stevilo2"))
            operacija = self.request.get("operacija")

            if operacija == "+":
                rezultat = num1 + num2
            elif operacija == "-":
                rezultat = num1 - num2
            elif operacija == "*":
                rezultat = num1 * num2
            elif operacija == "/":
                rezultat = num1 / num2
            params = {"rezultat":rezultat}
            return self.render_template("kalkulator.html", params=params)
        except:
            return self.render_template("kalkulator.html", params=params)