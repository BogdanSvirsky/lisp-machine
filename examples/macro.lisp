(defmacro twice (x)
    `(* ,x 2))

(print (twice 5))

(defmacro swap (a b)
    `(+ ,a ,b))

(print (swap 10 20))

(print "done")
