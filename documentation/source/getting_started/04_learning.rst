========
Learning
========

*This is a brief overview of a learning task. Requirements for a more specific task may vary substantially based on the goals or the data available to you.*

We now have ``bk.txt`` and ``facts.txt`` as a result of the previous step. In order to get show some results, we will construct a toy data set from predicates easily available in the facts file.

The *Delcaration of Independence* contains a set of phrases called the "List of Grievances", where the Founders spell out the 27 violations by King George III.

We can turn these into a text classification task where we learn the structure of the grievances.

Positive and Negative Examples
------------------------------

Labeling data is often a task of its own, but we will take a shortcut and label sentences beginning with **"He"** or **"For"** as being positive examples. Everything else is labeled as negative.

This is not exactly correct, but will be more than sufficient for this demonstration.

Create a train directory to store our training data.

.. code-block:: bash

  mkdir train

This combination of grep, awk, and sort finds all occurances of "He" and "For" in the facts; labels them as a positive example; and adds them to a train_pos.txt file.

.. code-block:: bash

  grep "'He'\|'For'" facts.txt |
    awk '{gsub("wordString","sentenceContainsTarget"); gsub("_[0-9]*,.*",")."); print}' |
    sort -u > train/train_pos.txt

This command does something similar, but returns all sentences *not* containing the example.

.. code-block:: bash

  grep "wordString" facts.txt |
    grep -v "'He'\|'For'" |
    awk '{gsub("wordString","sentenceContainsTarget"); gsub("_[0-9]*,.*",")."); print}' |
    sort -u > train/train_neg.txt

On closer inspection, we may realize that this method has double-counted some sentences. Some of the examples labeled as negative are also present in the positive examples. Luckily we can do a set difference to fix this.

.. code-block:: bash

  sort train/train_neg.txt train/train_pos.txt train/train_pos.txt | uniq -u

BoostSRL
--------

.. image:: ../_static/img/output.png

.. code-block:: bash

  mkdir train
  java -jar v1-0.jar -l -combine -train train/ -trees 25

The tree says that if the word string contained in word 'b' is "you" then 'b' is the word "you". (This is of course true).
A more interesting inference is the False branch that says that if word 'b' is an early word in sentence 'a' and word 'anon12035' is also an early word in sentence 'a' and if the word string contained in word 'anon12035' is "Thank", then the word 'b' has decent change of being the word "you". (The model was able to learn that the word "you" often occurs with the word "Thank" in the same sentence when "Thank" appears early in that sentence).
