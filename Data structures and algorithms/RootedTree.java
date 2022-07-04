import java.io.DataOutputStream;
import java.io.IOException;

public class RootedTree {
    GraphNode root;

    public RootedTree(){
    }

    public void printByLayer(DataOutputStream out) throws IOException {
        DoublyLinkedListNode Q1 = new DoublyLinkedListNode();
        GraphNode temp;
        GraphNode temp2;
        Q1.insertTailQ(root);
        GraphNode u=null;
        DoublyLinkedListNode Q2 = new DoublyLinkedListNode();
        while(Q1.getHead()!=null|| Q2.getHead()!=null){
            while(Q1.getHead()!=null) {
                out.writeBytes(""+Q1.getHead().getKey());
                u=Q1.getHead().leftChild;
                while(u!=null){
                    Q2.insertTailQ(u);
                    u=u.rightSibling;
                }
                Q1.deleteHeadQ(Q1.getHead());
                if(Q1.getHead()!=null)
                    out.writeBytes(",");
            }
            temp = Q1.head;
            temp2 = Q1.tail;
            Q1.head = Q2.head;
            Q1.tail = Q2.tail;
            Q2.head = temp;
            Q2.tail = temp2;

            if(Q1.getHead()!=null|| Q2.getHead()!=null)
                out.writeBytes("\n");
        }
    }

    public void preorderPrint(DataOutputStream out) throws IOException {
        if(this.root == null)
            return;
        out.writeBytes(""+root.getKey());
        RootedTree left =new RootedTree();
        if(root.leftChild !=null)
            out.writeBytes(",");
        else
            return;
        left.root = root.leftChild;
        left.preorderPrint(out);
        GraphNode node = root.leftChild.rightSibling;
        RootedTree right =new RootedTree();
        right.root = node;
        while(right.root != null) {
            out.writeBytes(",");
            right.preorderPrint(out);
            right.root = right.root.rightSibling;
        }
    }
}
