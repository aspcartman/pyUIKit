from ui.controller import Controller


class TestController:
    def test_next_responder(self):
        c1 = Controller()
        c2 = Controller()

        c1.view.add_subview(c2.view)
        assert c2.next_responder() == c1.view
        assert c1.view.next_responder() == c1
