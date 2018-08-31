========
Learning
========

*This is a brief overview of a learning task. Requirements for a more specific task may vary substantially based on the goals or the data available to you.*

.. image:: ../_static/img/output.png

.. code-block:: bash

  mkdir train
  java -jar v1-0.jar -l -combine -train train/ -trees 25

The tree says that if the word string contained in word 'b' is "you" then 'b' is the word "you". (This is of course true).
A more interesting inference is the False branch that says that if word 'b' is an early word in sentence 'a' and word 'anon12035' is also an early word in sentence 'a' and if the word string contained in word 'anon12035' is "Thank", then the word 'b' has decent change of being the word "you". (The model was able to learn that the word "you" often occurs with the word "Thank" in the same sentence when "Thank" appears early in that sentence).
