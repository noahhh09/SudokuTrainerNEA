/**
 * A generic stack that supports any type of class, T.
 */
export class Stack<T> {
    private items: T[] = []

    push(item: T) {
        this.items.push(item)
    }

    pop(): T | undefined {
        return this.items.pop()
    }

    peek(): T | undefined {
        return this.items[this.items.length - 1]
    }

    isEmpty(): boolean {
        return this.items.length == 0
    }
}