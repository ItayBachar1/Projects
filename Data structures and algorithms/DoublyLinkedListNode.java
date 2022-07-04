public class DoublyLinkedListNode {
    GraphNode head;
    GraphNode tail;

    public void insertHead(GraphNode value) {
        value.next = this.head;
        if (this.head == null) {
            this.tail = value;
        }
        else {
            this.head.prev = value;
        }
        this.head = value;
        value.prev = null;
    }

    public void insertHeadQ(GraphNode value) {
        value.nextQ = this.head;
        if (this.head == null) {
            this.tail = value;
        }
        else {
            this.head.prevQ = value;
        }
        this.head = value;
        value.prevQ = null;
    }



    public void insertTail(GraphNode value) {
        value.prev = this.tail;
        if(this.tail==null){
            this.head=value;
        }
        else{
            this.tail.next = value;
        }
        this.tail=value;
        this.tail.next = null;

    }

    public void insertTailQ(GraphNode value) {
        value.prevQ = this.tail;
        if(this.tail==null){
            this.head=value;
        }
        else{
            this.tail.nextQ = value;
        }
        this.tail=value;
        this.tail.nextQ = null;

    }

    public void deleteNode(GraphNode node) {
        if(node==null)
            return;
        if(node.next!=null){
            if(node.prev!=null){
                node.prev.next = node.next;
                node.next.prev = node.prev;
            }
            else{
                node.next.prev = null;
                this.head = node.next;
            }
        }
        else{
            if(node.prev!=null){
                node.prev.next = null;
                this.tail = node.prev;
            }
            else{
                this.head=null;
                this.tail=null;
            }
        }
        node.next =null;
        node.prev =null;
    }

    public void deleteHeadQ(GraphNode node) {
        if(node==null)
            return;
        if(node.nextQ!=null){
            if(node.prevQ!=null){
                node.prevQ.nextQ = node.nextQ;
                node.nextQ.prevQ = node.prevQ;
            }
            else{
                node.nextQ.prevQ = null;
                this.head = node.nextQ;
            }
        }
        else{
            if(node.prevQ!=null){
                node.prevQ.nextQ = null;
                this.tail = node.prevQ;
            }
            else{
                this.head=null;
                this.tail=null;
            }
        }
        node.nextQ =null;
        node.prevQ =null;
    }

    public void deleteHead() {
        deleteNode(this.head);
    }

    public void deleteTail() {
        deleteNode(this.tail);
    }

    public GraphNode getHead() {
        return this.head;
    }

    public GraphNode getTail() {
        return this.tail;
    }

}
