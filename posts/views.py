import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from rest_framework import generics, viewsets
from rest_framework.views import Response, status

from .models import Post, Source
from .serializers import PostDetailSerializer, PostListSerializer, SourceSerializer


class SourceViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Source.objects.filter(active=True)
    serializer_class = SourceSerializer


class PostViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return super().get_serializer_class()


class SummarisePostView(generics.GenericAPIView):
    queryset = Post.objects.filter(is_summarised=False, has_body=True)

    def get(self, request, *args, **kwargs):
        if queryset := self.get_queryset():
            try:
                for post in queryset:
                    post.body = self.summarise_content(post.body, 5)
                    post.is_summarised = True
                    post.save()

                return Response(
                    {
                        "status": "success",
                        "message": f"{queryset.count()} posts have been added sucessfully"
                    },
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"status": "success",
                        "message": f"An error occurred {(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response({"status": "success", "message": "No new posts"}, status=status.HTTP_200_OK)

    def summarise_content(self, text, num_sentences=5):
        """
        Summarises the content of a given text by extracting
        the most important sentences.

        Args:
            text (str): The text to be summarized.
            num_sentences (int): The number of sentences to include in the summary.

        Returns:
            str: The summarized content.
        """
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        # extract individual sentences from tokenized document
        sentences = [sent.text for sent in doc.sents]

        # Create TF-IDF vectorizer to convert sentences into numerical vectors
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(sentences)

        # calculate sum of cosine similarity scores for each sentence
        similarity_matrix = cosine_similarity(X, X)
        scores = similarity_matrix.sum(axis=1)

        # identify top 'num_sentences' sentences based on scores
        top_indices = scores.argsort()[-num_sentences:][::-1]
        top_indices.sort()

        summary = ' '.join([sentences[i] for i in top_indices])

        # summarise text again if summary is too long
        if len(summary.split()) > 220:
            return self.summarise_content(summary, num_sentences-1)

        return summary
